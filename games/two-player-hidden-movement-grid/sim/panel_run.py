"""Panel rotation for Dead Reckoning: every pair of the 6 personas plays in both seats (2-player game, so no filler bots).
Writes sim/panel-results.json (input for panel/scoring.py) and sample logs sim/logs/<persona>-1.txt / -2.txt.
Usage: python3 panel_run.py [games_per_seating=200]"""
import itertools, json, os, sys
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "panel"))
from game import Config, play
import bots as B
import scoring as S

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SLUG = "two-player-hidden-movement-grid"
PERSONAS = S.load_personas(ROOT)
IDS = sorted(PERSONAS)
BRIEF = json.load(open(os.path.join(ROOT, "games", SLUG, "brief.json")))

class Count:
    def __init__(self, bot): self.bot = bot; self.n = 0
    def want_ping(self, g, me): self.n += 1; return self.bot.want_ping(g, me)
    def plot(self, g, me, hand, known): self.n += 3; return self.bot.plot(g, me, hand, known)   # three ordered card choices

def one_game(a, b, seed, log=False):
    ca, cb = Count(B.PERSONA[a](seed)), Count(B.PERSONA[b](seed + 1))
    r = play(Config(log=log), (ca, cb), seed); g = r["game"]; st = g.s; w = r["winner"]
    sg = [x for x in ((d > 0) - (d < 0) for d in g.history) if x]
    lc = sum(1 for x, y in zip(sg, sg[1:]) if x != y)
    rs = g.round_scores; mid = rs[(len(rs) - 1) // 2] if rs else 0
    hits = sum(st.stats["hits"]); out = []
    for seat, c in ((0, ca), (1, cb)):
        trailed = bool(mid) and ((mid < 0) if seat == 0 else (mid > 0))
        out.append(dict(won=1.0 if w == seat else 0.5 if w is None else 0.0, turns=r["rounds"], decisions=c.n, lead_changes=lc,
                        trailed=int(trailed), comeback=int(trailed and w == seat), hits=hits, opp_decisions=0))
    return out, st

def table(job):
    a, b, per, seed = job
    rows = {a: [], b: []}; seat = {a: {0: [], 1: []}, b: {0: [], 1: []}}
    for k in range(2 * per):
        first, second = (a, b) if k < per else (b, a)
        out, _ = one_game(first, second, seed + k)
        for s, who in enumerate((first, second)): rows[who].append(out[s]); seat[who][s].append(out[s])
    return (a, b), rows, seat

def agg(rows):
    n = len(rows); t = sum(r["turns"] for r in rows) or 1; tr = sum(r["trailed"] for r in rows)
    return {"games": n, "win_rate": sum(r["won"] for r in rows) / n, "decisions_per_turn": sum(r["decisions"] for r in rows) / t,
            "lead_changes": sum(r["lead_changes"] for r in rows) / n, "comeback_rate": (sum(r["comeback"] for r in rows) / tr) if tr else 0.0,
            "fell_behind_rate": sum(1 for r in rows if r["trailed"] and r["won"] < 1) / n,
            "interaction_rate": sum(r["hits"] for r in rows) / t, "downtime": 0.0}   # simultaneous plotting: nobody waits (ping rounds aside)

def main(per=200):
    playtest = json.load(open(os.path.join(ROOT, "games", SLUG, "playtest.json")))
    words = len(open(os.path.join(ROOT, "games", SLUG, "rules.md"), encoding="utf-8").read().split())
    pairs = list(itertools.combinations(IDS, 2))
    jobs = [(a, b, per, 1000 * (IDS.index(a) * 10 + IDS.index(b))) for a, b in pairs]
    with Pool(4) as pool: res = pool.map(table, jobs)
    by_p = {i: [] for i in IDS}; by_seat = {i: {0: [], 1: []} for i in IDS}; tables = {}
    for (a, b), rows, seat in res:
        tables[(a, b)] = rows
        for who in (a, b):
            by_p[who] += rows[who]
            for s in (0, 1): by_seat[who][s] += seat[who][s]
    metrics_of = lambda who, rows: {**S.game_metrics(playtest, words, PERSONAS[who]["preferred_minutes"], BRIEF), **S.bot_metrics(agg(rows))}
    fun_at = lambda who, rows: S.fun_from_metrics(metrics_of(who, rows), PERSONAS[who]["weights"])
    personas, matchups = {}, []
    for (a, b), rows in tables.items():
        ra, rb = agg(rows[a]), agg(rows[b])
        matchups.append({"a": a, "b": b, "games": len(rows[a]), "a_win_rate": round(ra["win_rate"], 3), "note": "", "a_raw": ra, "b_raw": rb})
    os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
    for who in IDS:
        opts = [(fun_at(who, tables[tuple(sorted((who, o)))][who]), o) for o in IDS if o != who]
        best, worst = max(opts), min(opts); raw = agg(by_p[who])
        personas[who] = {"raw": raw, "best_table": sorted([who, best[1]]), "worst_table": sorted([who, worst[1]]),
                         "bot": {"win_rate": round(raw["win_rate"], 3), "fell_behind_rate": round(raw["fell_behind_rate"], 3),
                                 "decisions_per_turn": round(raw["decisions_per_turn"], 2), "downtime": 0.0, "games": raw["games"],
                                 "seat_win_rates": {str(s + 1): round(agg(by_seat[who][s])["win_rate"], 3) for s in (0, 1)}}}
        for n, (_, o) in enumerate((best, worst), 1):
            _, st = one_game(who, o, 777 + n, log=True)
            with open(os.path.join(HERE, "logs", "%s-%d.txt" % (who, n)), "w") as f:
                f.write("Dead Reckoning: %s (seat 1, Blue) vs %s (seat 2, Red), %s table for %s. Squares A-E x 1-5.\n" % (who, o, "best" if n == 1 else "worst", who))
                f.write("\n".join(st.log[:40]) + "\n")
    out = {"personas": personas, "matchups": matchups,
           "rotation": {"player_counts": [2], "tables": len(tables), "seatings_per_table": 2, "games_per_seating": per, "filler_bots": []}}
    json.dump(out, open(os.path.join(HERE, "panel-results.json"), "w"), indent=1)
    print("rotation: %d tables x 2 seatings x %d games; each persona played %d games" % (len(tables), per, len(by_p[IDS[0]])))

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 200)
