"""Panel rotation for Silent Duo (co-op): every pair of the six personas as a team (both seatings), plus every trio
(3 cyclic seatings). 200 games per seating, fixed seeds. Writes sim/panel-results.json and sim/logs/<persona>-1|2.txt.
Usage: python3 panel_run.py [games_per_seating=200]"""
import itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "panel"))
from game import Game, play
import bots as B
import scoring as S

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SLUG = "silent-duo-deduction-coop"
PERSONAS = S.load_personas(ROOT)
IDS = ["casual", "competitor", "family", "story", "strategist", "barraiser"]
BRIEF = json.load(open(os.path.join(ROOT, "games", SLUG, "brief.json")))
FOG = {2: 6, 3: 2}      # rules.md Standard

def one(seats, seed, log=False):
    n = len(seats)
    g = Game(n, FOG[n], seed, log=log)
    bs = [B.PERSONA[p](seed * 13 + k) for k, p in enumerate(seats)]
    play(g, bs)
    tl = g.timeline
    sw = sum(1 for a, b in zip(tl, tl[1:]) if a != b)
    risk = any(tl)
    out = []
    for k, p in enumerate(seats):
        out.append(dict(won=int(g.win), turns=g.turns, decisions=g.dec[k] / max(1, g.turns / n) * (g.turns / max(1, g.turns)),
                        lead_changes=sw, trailed=int(risk), comeback=int(risk and g.win),
                        busts=g.stats["offers"], bait=0, opp_decisions=sum(g.dec) - g.dec[k], offers=g.stats["offers"]))
    return out, g

def agg(rows):
    n = len(rows); t = sum(r["turns"] for r in rows) or 1; tr = sum(r["trailed"] for r in rows)
    return {"games": n, "win_rate": sum(r["won"] for r in rows) / n,
            "decisions_per_turn": sum(r["decisions"] for r in rows) / n,
            "lead_changes": sum(r["lead_changes"] for r in rows) / n,
            "comeback_rate": (sum(r["comeback"] for r in rows) / tr) if tr else 0.0,
            "fell_behind_rate": sum(1 for r in rows if r["trailed"] and not r["won"]) / n,
            "interaction_rate": sum(r["busts"] for r in rows) / t,
            "downtime": sum(r["opp_decisions"] for r in rows) / t}

def main(per=200):
    playtest = json.load(open(os.path.join(ROOT, "games", SLUG, "playtest.json")))
    words = len(open(os.path.join(ROOT, "games", SLUG, "rules.md"), encoding="utf-8").read().split())
    by_p = {i: [] for i in IDS}; by_p3 = {i: [] for i in IDS}; by_seat = {i: {0: [], 1: []} for i in IDS}
    tables = {}; seed = 0
    for a, b in itertools.combinations(IDS, 2):
        rows = {a: [], b: []}
        for first, second in ((a, b), (b, a)):
            for k in range(per):
                seed += 1
                out, _ = one((first, second), 100000 + seed)
                for s, who in enumerate((first, second)):
                    rows[who].append(out[s]); by_p[who].append(out[s]); by_seat[who][s].append(out[s])
        tables[(a, b)] = rows
    t3 = {}
    for trio in itertools.combinations(IDS, 3):
        rr = []
        for rot in range(3):
            seats = trio[rot:] + trio[:rot]
            for k in range(per):
                seed += 1
                out, _ = one(seats, 100000 + seed)
                rr.append(out[0]["won"])
                for s, who in enumerate(seats): by_p3[who].append(out[s]["won"])
        t3["+".join(trio)] = round(sum(rr) / len(rr), 3)
    metrics_of = lambda who, rows: {**S.game_metrics(playtest, words, PERSONAS[who]["preferred_minutes"], BRIEF), **S.bot_metrics(agg(rows))}
    fun_at = lambda who, rows: S.fun_from_metrics(metrics_of(who, rows), PERSONAS[who]["weights"])
    personas, matchups = {}, []
    for (a, b), rows in tables.items():
        matchups.append({"a": a, "b": b, "games": len(rows[a]), "a_win_rate": round(agg(rows[a])["win_rate"], 3),
                         "note": "co-op: team win rate", "a_raw": agg(rows[a]), "b_raw": agg(rows[b])})
    os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
    for who in IDS:
        opts = [(fun_at(who, tables[tuple(x for x in IDS if x in (who, o))][who]), o) for o in IDS if o != who]
        best, worst = max(opts), min(opts)
        raw = agg(by_p[who])
        personas[who] = {"raw": raw, "best_table": sorted([who, best[1]]), "worst_table": sorted([who, worst[1]]),
                         "bot": {"win_rate": round(raw["win_rate"], 3), "fell_behind_rate": round(raw["fell_behind_rate"], 3),
                                 "decisions_per_turn": round(raw["decisions_per_turn"], 2), "downtime": round(raw["downtime"], 2),
                                 "games": raw["games"], "team_win_rate_3p": round(sum(by_p3[who]) / len(by_p3[who]), 3),
                                 "seat_win_rates": {str(s + 1): round(agg(by_seat[who][s])["win_rate"], 3) for s in (0, 1)}}}
        for n, (_, o) in enumerate((best, worst), 1):
            _, g = one((who, o), 777 + n, log=True)
            with open(os.path.join(HERE, "logs", "%s-%d.txt" % (who, n)), "w") as f:
                f.write("Silent Duo: team %s (seat 1) + %s (seat 2), table '%s' for %s. Events: offer <by> <owner> <ship> <shown> <row>; light <by> <ship> <card> <ship value> <beacon>.\n" % (who, o, "best" if n == 1 else "worst", who))
                f.write("\n".join(g.log[:40]) + "\nResult: %s after %d turns\n" % ("WIN" if g.win else "LOSS", g.turns))
    out = {"personas": personas, "matchups": matchups,
           "rotation": {"player_counts": [2, 3], "tables": len(tables), "tables_3p": len(t3), "seatings_per_table": 2,
                        "seatings_per_table_3p": 3, "games_per_seating": per, "filler_bots": [],
                        "note": "co-op: every pair is one team in both seatings; every trio in 3 cyclic seatings. Raw metrics use 2-player games only; 3-player team win rates in bot.team_win_rate_3p. fell_behind_rate = share of games lost after the team was at risk (two Reefs gone, or fewer than 3 turns left per unlit ship). lead_changes = swings in/out of at-risk. interaction_rate = Offers per turn.",
                        "trio_win_rates": t3}}
    json.dump(out, open(os.path.join(HERE, "panel-results.json"), "w"), indent=1)
    print("rotation: %d pair tables x2 seatings, %d trio tables x3 seatings, %d games each" % (len(tables), len(t3), per))

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 200)
