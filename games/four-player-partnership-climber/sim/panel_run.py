"""Panel rotation for Ladder Pairs (4 players). 6 personas -> 15 four-persona tables x 4 cyclic seatings x games_per_seating games.
Writes sim/panel-results.json and sim/logs/<persona>-1.txt / -2.txt. Usage: python3 panel_run.py [games_per_seating=200]"""
import itertools, json, os, sys
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "panel")); sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools", "sim-kit"))
import game as Gm
import bots as B
import scoring as S
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SLUG = "four-player-partnership-climber"
PERSONAS = S.load_personas(ROOT)
FIRST = ["casual", "competitor", "family", "story", "strategist"]
IDS = FIRST + sorted(set(PERSONAS) - set(FIRST))
BRIEF = json.load(open(os.path.join(ROOT, "games", SLUG, "brief.json")))


def one_game(table, seating, seed, log=False):
    """table: 4 persona ids; seating: rotation k (persona i sits in seat (i+k)%4)."""
    seat_of = {who: (i + seating) % 4 for i, who in enumerate(table)}
    order = [None] * 4
    for who, s in seat_of.items(): order[s] = who
    bots = [B.PERSONA[w](seed * 7 + s) for s, w in enumerate(order)]
    r = Gm.play(bots, seed, Gm.Cfg(log=log))
    H = r["hands"]; out = {}
    cum = [sum(h["pts"][q] for h in H[:3]) for q in range(4)]
    mx = max(cum)
    lc = simkit_lc(r["leaders"])
    tot_turns = r["turns"]
    for s, who in enumerate(order):
        trailed = cum[s] < mx
        turns = sum(h["turns_by"][s] for h in H) or 1
        out[who] = dict(won=int(r["winner"] == s), turns=turns, decisions=sum(h["decisions"][s] for h in H), lead_changes=lc,
                        trailed=int(trailed), comeback=int(trailed and r["winner"] == s), beats=sum(h["beats"][s] for h in H),
                        others_turns=tot_turns - turns, seat=s)
    return out, r, order


def simkit_lc(L):
    seen = [x for x in L if x is not None]
    return sum(1 for a, b in zip(seen, seen[1:]) if a != b)


def run_table(args):
    table, per = args
    rows = {w: [] for w in table}
    base = 100000 * (1 + sum(IDS.index(w) * 10 ** i for i, w in enumerate(table)) % 9973)
    for k in range(4):
        for g in range(per):
            out, _, _ = one_game(table, k, base + k * per + g)
            for w, o in out.items(): rows[w].append(o)
    return table, rows


def agg(rows):
    n = len(rows); t = sum(r["turns"] for r in rows) or 1; tr = sum(r["trailed"] for r in rows)
    return {"games": n, "win_rate": sum(r["won"] for r in rows) / n, "decisions_per_turn": sum(r["decisions"] for r in rows) / t,
            "lead_changes": sum(r["lead_changes"] for r in rows) / n, "comeback_rate": (sum(r["comeback"] for r in rows) / tr) if tr else 0.0,
            "fell_behind_rate": sum(1 for r in rows if r["trailed"] and not r["won"]) / n,
            "interaction_rate": sum(r["beats"] for r in rows) / t, "downtime": sum(r["others_turns"] for r in rows) / t}


def main(per=200):
    playtest = json.load(open(os.path.join(ROOT, "games", SLUG, "playtest.json")))
    words = len(open(os.path.join(ROOT, "games", SLUG, "rules.md"), encoding="utf-8").read().split())
    tables = list(itertools.combinations(IDS, 4))
    with Pool(4) as pool: res = pool.map(run_table, [(t, per) for t in tables])
    by_p = {i: [] for i in IDS}; by_seat = {i: {s: [] for s in range(4)} for i in IDS}; tab = {}
    for table, rows in res:
        tab[table] = rows
        for w, rs in rows.items():
            by_p[w] += rs
            for r in rs: by_seat[w][r["seat"]].append(r)
    metrics_of = lambda who, rows: {**S.game_metrics(playtest, words, PERSONAS[who]["preferred_minutes"], BRIEF), **S.bot_metrics(agg(rows))}
    fun_at = lambda who, rows: S.fun_from_metrics(metrics_of(who, rows), PERSONAS[who]["weights"])
    personas, matchups = {}, []
    for table, rows in tab.items():
        for a, b in itertools.combinations(table, 2):
            pass
    pair_rows = {}
    for table, rows in tab.items():
        for a in table:
            for b in table:
                if a < b: pair_rows.setdefault((a, b), {a: [], b: []}); pair_rows[(a, b)][a] += rows[a]; pair_rows[(a, b)][b] += rows[b]
    for (a, b), rows in pair_rows.items():
        ra, rb = agg(rows[a]), agg(rows[b])
        matchups.append({"a": a, "b": b, "games": len(rows[a]), "a_win_rate": round(ra["win_rate"], 3), "note": "pairing = both seated at the same 4-persona tables", "a_raw": ra, "b_raw": rb})
    for who in IDS:
        opts = [(fun_at(who, tab[t][who]), t) for t in tab if who in t]
        best, worst = max(opts), min(opts)
        raw = agg(by_p[who])
        personas[who] = {"raw": raw, "best_table": sorted(best[1]), "worst_table": sorted(worst[1]),
                         "bot": {"win_rate": round(raw["win_rate"], 3), "fell_behind_rate": round(raw["fell_behind_rate"], 3),
                                 "decisions_per_turn": round(raw["decisions_per_turn"], 2), "downtime": round(raw["downtime"], 2), "games": raw["games"],
                                 "seat_win_rates": {str(s + 1): round(agg(by_seat[who][s])["win_rate"], 3) for s in range(4)}}}
        os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
        for n, (_, t) in enumerate((best, worst), 1):
            _, r, order = one_game(t, 0, 777 + n, log=True)
            with open(os.path.join(HERE, "logs", "%s-%d.txt" % (who, n)), "w") as f:
                f.write("Ladder Pairs: seats 0-3 = %s; table '%s' for %s. S@n = single rank n, P pair, T triple, R run (n cards, top rank); Rope = rank 14/15.\n"
                        % (order, "best" if n == 1 else "worst", who))
                f.write("\n".join(r["hands"][0]["log"][:45]) + "\n")
    out = {"personas": personas, "matchups": matchups,
           "rotation": {"player_counts": [4], "tables": len(tab), "seatings_per_table": 4, "games_per_seating": per, "filler_bots": []}}
    with open(os.path.join(HERE, "panel-results.json"), "w") as f: json.dump(out, f, indent=1); f.write("\n")
    print("rotation: %d tables x 4 seatings x %d games; games per persona %d" % (len(tab), per, len(by_p[IDS[0]]) // 4))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 200)
