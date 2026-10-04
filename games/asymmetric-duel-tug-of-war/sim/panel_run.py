"""Panel rotation for Tug of Crowns (2 players only): every pair of the six personas, both sides, same games per persona.
Seat 1 = Treasurer, seat 2 = Whisperer. Writes panel-results.json and logs/<persona>-1.txt / -2.txt.
Usage: python3 panel_run.py [games_per_seating=200]"""
import itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "panel"))
from game import play
import bots as B
import scoring as S

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
G = os.path.join(ROOT, "games", "asymmetric-duel-tug-of-war")
PERSONAS = S.load_personas(ROOT)
FIRST = ["casual", "competitor", "family", "story", "strategist"]
IDS = FIRST + sorted(set(PERSONAS) - set(FIRST))
BRIEF = json.load(open(os.path.join(G, "brief.json")))

class Count:
    def __init__(self, bot): self.bot = bot; self.n = 0; self.turns = 0
    def __getattr__(self, k): return getattr(self.bot, k)
    def choose(self, st, p, acts, retort=False):
        self.turns += 1
        if len(acts) >= 3 or retort: self.n += 1       # a real choice: more than pass vs one forced card
        return self.bot.choose(st, p, acts, retort)
    def choose_lead(self, st, p): self.n += 1; return self.bot.choose_lead(st, p)

def one_game(a, b, seed, log=False):
    """a is the Treasurer (seat 1), b the Whisperer (seat 2)."""
    ca, cb = Count(B.PERSONA[a](seed)), Count(B.PERSONA[b](seed + 1))
    r = play((ca, cb), seed, log=log); st = r["st"]; h = st.history; w = r["winner"]
    sg = [x for x in ((d > 0) - (d < 0) for d in h) if x]
    lc = sum(1 for x, y in zip(sg, sg[1:]) if x != y)
    mid = h[len(h) // 2] if h else 0
    s = st.stats; inter = s["hush"] - s["hush_blank"] + s["retort"]
    out = []
    for seat, c in ((0, ca), (1, cb)):
        trailed = bool(mid) and ((mid > 0) if seat == 0 else (mid < 0))   # pos<0 = Treasurer side
        out.append(dict(won=int(w == seat), turns=c.turns, all_turns=ca.turns + cb.turns, decisions=c.n, lead_changes=lc,
                        trailed=int(trailed), comeback=int(trailed and w == seat), inter=inter,
                        opp_decisions=(cb if seat == 0 else ca).n))
    return out, st

def agg(rows):
    n = len(rows); t = sum(r["turns"] for r in rows) or 1; tr = sum(r["trailed"] for r in rows)
    at = sum(r["all_turns"] for r in rows) or 1
    return {"games": n, "win_rate": sum(r["won"] for r in rows) / n,
            "decisions_per_turn": sum(r["decisions"] for r in rows) / t,
            "lead_changes": sum(r["lead_changes"] for r in rows) / n,
            "comeback_rate": (sum(r["comeback"] for r in rows) / tr) if tr else 0.0,
            "fell_behind_rate": sum(1 for r in rows if r["trailed"] and not r["won"]) / n,
            "interaction_rate": sum(r["inter"] for r in rows) / at,
            "downtime": sum(r["opp_decisions"] for r in rows) / t}

def main(per_seating=200):
    playtest = json.load(open(os.path.join(G, "playtest.json")))
    words = len(open(os.path.join(G, "rules.md"), encoding="utf-8").read().split())
    by_p = {i: [] for i in IDS}; by_seat = {i: {0: [], 1: []} for i in IDS}; tables = {}
    for a, b in itertools.combinations(IDS, 2):
        rows = {a: [], b: []}; seed = 1000 * (IDS.index(a) * 10 + IDS.index(b))
        for k in range(2 * per_seating):
            first, second = (a, b) if k < per_seating else (b, a)
            out, _ = one_game(first, second, seed + k)
            for seat, who in enumerate((first, second)):
                rows[who].append(out[seat]); by_p[who].append(out[seat]); by_seat[who][seat].append(out[seat])
        tables[tuple(sorted((a, b)))] = rows
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
                                 "decisions_per_turn": round(raw["decisions_per_turn"], 2), "downtime": round(raw["downtime"], 2),
                                 "games": raw["games"],
                                 "seat_win_rates": {str(s + 1): round(agg(by_seat[who][s])["win_rate"], 3) for s in (0, 1)}}}
        for n, (_, o) in enumerate((best, worst), 1):
            _, st = one_game(who, o, 777 + n, log=True)
            with open(os.path.join(HERE, "logs", "%s-%d.txt" % (who, n)), "w") as f:
                f.write("Tug of Crowns: %s (Treasurer) vs %s (Whisperer), %s table for %s. Crown pos: negative = Treasurer side.\n"
                        % (who, o, "best" if n == 1 else "worst", who))
                f.write("\n".join(st.log[:45]) + "\n")
    out = {"personas": personas, "matchups": matchups,
           "rotation": {"player_counts": [2], "tables": len(tables), "seatings_per_table": 2,
                        "games_per_seating": per_seating, "filler_bots": []}}
    json.dump(out, open(os.path.join(HERE, "panel-results.json"), "w"), indent=1)
    print("rotation: %d tables x 2 seatings x %d games; games per persona %d" % (len(tables), per_seating, len(by_p[IDS[0]])))

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 200)
