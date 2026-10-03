"""Panel rotation for Split the Take (exactly 3 players). Every triple of personas, all 6 seatings, N games each.
Writes sim/panel-results.json and sim/logs/<persona>-1.txt / -2.txt. Usage: python3 panel_run.py [games_per_seating=200]"""
import itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "panel"))
from game import Game
import bots as B
import scoring as S

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SLUG = "three-player-trick-taker"
PERSONAS = S.load_personas(ROOT)
IDS = sorted(PERSONAS)

def one_game(trio, seed, log=False):
    """trio: persona ids by seat. Returns (per-seat rows, game)."""
    g = Game([B.PERSONA[p](seed + i) for i, p in enumerate(trio)], seed, log=log).run()
    cum = [0, 0, 0]
    for r in g.rec[:3]:
        for i in range(3): cum[i] += r["pts"][i]
    top = max(cum); rows = []
    for i in range(3):
        trailed = cum[i] < top
        w = 1.0 / len(g.winners) if i in g.winners else 0.0
        rows.append(dict(won=w, turns=g.turns[i], decisions=g.decisions[i], lead_changes=len([1 for a, b in zip(*(lambda s: (s, s[1:]))([x for x in g.lead_seq if x is not None])) if a != b]),
                         trailed=int(trailed), comeback=w if trailed else 0.0, trailed_lost=int(trailed) * (1 - w),
                         inter=(g.ruffs + sum(g.dc_wins)) / g.tricks_played * g.turns[i],
                         opp_decisions=sum(g.decisions) - g.decisions[i]))
    return rows, g

def agg(rows):
    n = len(rows); t = sum(r["turns"] for r in rows) or 1; tr = sum(r["trailed"] for r in rows)
    return {"games": n, "win_rate": sum(r["won"] for r in rows) / n,
            "decisions_per_turn": sum(r["decisions"] for r in rows) / t,
            "lead_changes": sum(r["lead_changes"] for r in rows) / n,
            "comeback_rate": (sum(r["comeback"] for r in rows) / tr) if tr else 0.0,
            "fell_behind_rate": sum(r["trailed_lost"] for r in rows) / n,
            "interaction_rate": sum(r["inter"] for r in rows) / t,
            "downtime": sum(r["opp_decisions"] for r in rows) / t}

def main(per=200):
    playtest = json.load(open(os.path.join(ROOT, "games", SLUG, "playtest.json")))
    words = len(open(os.path.join(ROOT, "games", SLUG, "rules.md"), encoding="utf-8").read().split())
    by_p = {i: [] for i in IDS}; by_seat = {i: {0: [], 1: [], 2: []} for i in IDS}; tables = {}
    for ti, trio in enumerate(itertools.combinations(IDS, 3)):
        rows = {p: [] for p in trio}
        for pi, perm in enumerate(itertools.permutations(trio)):
            for k in range(per):
                out, _ = one_game(perm, 1000 * ti + 100000 * pi + k)
                for seat, who in enumerate(perm):
                    rows[who].append(out[seat]); by_p[who].append(out[seat]); by_seat[who][seat].append(out[seat])
        tables[trio] = rows
    metrics_of = lambda who, rows: {**S.game_metrics(playtest, words, PERSONAS[who]["preferred_minutes"]), **S.bot_metrics(agg(rows))}
    fun_at = lambda who, rows: S.fun_from_metrics(metrics_of(who, rows), PERSONAS[who]["weights"])
    personas = {}; os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
    for who in IDS:
        opts = [(fun_at(who, rows[who]), trio) for trio, rows in tables.items() if who in trio]
        best, worst = max(opts), min(opts); raw = agg(by_p[who])
        personas[who] = {"raw": raw, "best_table": list(best[1]), "worst_table": list(worst[1]),
                         "bot": {"win_rate": round(raw["win_rate"], 3), "fell_behind_rate": round(raw["fell_behind_rate"], 3),
                                 "decisions_per_turn": round(raw["decisions_per_turn"], 2), "downtime": round(raw["downtime"], 2),
                                 "games": raw["games"], "seat_win_rates": {str(s + 1): round(agg(by_seat[who][s])["win_rate"], 3) for s in range(3)}}}
        for n, (_, trio) in enumerate((best, worst), 1):
            perm = (who,) + tuple(x for x in trio if x != who)
            _, g = one_game(perm, 777 + n, log=True)
            with open(os.path.join(HERE, "logs", "%s-%d.txt" % (who, n)), "w") as f:
                f.write("Split the Take: seats 0,1,2 = %s; table '%s' for %s. Cards: Co/Ge/Ke/Ma + rank. Scores after each round in header.\n"
                        % (", ".join(perm), "best" if n == 1 else "worst", who))
                f.write("\n".join(g.log[:45]) + "\nFinal %s winners %s\n" % (g.scores, g.winners))
    matchups = []
    for a, b in itertools.combinations(IDS, 2):
        ra = [r for trio, rows in tables.items() if a in trio and b in trio for r in rows[a]]
        rb = [r for trio, rows in tables.items() if a in trio and b in trio for r in rows[b]]
        matchups.append({"a": a, "b": b, "games": len(ra), "a_win_rate": round(agg(ra)["win_rate"], 3),
                         "note": "3-player: averaged over the 3 tables containing both", "a_raw": agg(ra), "b_raw": agg(rb)})
    out = {"personas": personas, "matchups": matchups,
           "rotation": {"player_counts": [3], "tables": len(tables), "seatings_per_table": 6, "games_per_seating": per, "filler_bots": []}}
    json.dump(out, open(os.path.join(HERE, "panel-results.json"), "w"), indent=1)
    print("rotation: %d tables x 6 seatings x %d games; games per persona %d" % (len(tables), per, len(by_p[IDS[0]])))

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 200)
