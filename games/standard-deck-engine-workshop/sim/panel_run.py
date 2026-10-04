"""Panel rotation for Fifty-Two Workshop. Tables of 2, 3 and 4 personas (all combinations), cyclic seat rotation,
G games per seating. Writes sim/panel-results.json and sim/logs/<persona>-1.txt (best table) / -2.txt (worst table).
Usage: python3 panel_run.py [games_per_seating=200]"""
import itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "panel"))
from game import *
import bots as B
import scoring as S
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SLUG = "standard-deck-engine-workshop"
PERSONAS = S.load_personas(ROOT)
FIRST = ["casual", "competitor", "family", "story", "strategist"]
IDS = [i for i in FIRST + sorted(set(PERSONAS) - set(FIRST)) if i in B.PERSONA]
BRIEF = json.load(open(os.path.join(ROOT, "games", SLUG, "brief.json")))

def one_game(order, seed, log=False):
    n = len(order); cfg = Config(n=n, log=log)
    r = play(cfg, [B.PERSONA[o](seed * 10 + i) for i, o in enumerate(order)], seed); st = r["st"]; w = r["winners"]
    h = st.rounds_hist; ld = []
    for sc in h:
        m = max(sc); lead = [i for i, s in enumerate(sc) if s == m]; ld.append(lead[0] if len(lead) == 1 else None)
    nz = [x for x in ld if x is not None]; lc = sum(1 for a, b in zip(nz, nz[1:]) if a != b)
    mid = h[len(h) // 2] if h else None
    rows = []
    for i in range(n):
        trailed = bool(mid) and mid[i] < max(mid); won = (1.0 / len(w)) if i in w else 0.0
        opp_dec = sum(st.dec) - st.dec[i]
        rows.append(dict(won=won, turns=st.turns[i], decisions=st.dec[i], lead_changes=lc, trailed=int(trailed), comeback=int(trailed and won > 0.5),
                         inter=st.inter[i], opp_decisions=opp_dec))
    return rows, st

def agg(rows):
    n = len(rows); t = sum(r["turns"] for r in rows) or 1; tr = sum(r["trailed"] for r in rows)
    return {"games": n, "win_rate": sum(r["won"] for r in rows) / n, "decisions_per_turn": sum(r["decisions"] for r in rows) / t,
            "lead_changes": sum(r["lead_changes"] for r in rows) / n,
            "comeback_rate": (sum(r["comeback"] for r in rows) / tr) if tr else 0.0,
            "fell_behind_rate": sum(1 for r in rows if r["trailed"] and r["won"] < 0.5) / n,
            "interaction_rate": sum(r["inter"] for r in rows) / t,
            "downtime": sum(r["opp_decisions"] for r in rows) / t}     # opponents' decisions between two of my turns

def main(G=200):
    playtest = json.load(open(os.path.join(ROOT, "games", SLUG, "playtest.json")))
    words = len(open(os.path.join(ROOT, "games", SLUG, "rules.md"), encoding="utf-8").read().split())
    by_p = {i: [] for i in IDS}; by_seat = {i: {} for i in IDS}; tables = {}
    for k in (2, 3, 4):
        for combo in itertools.combinations(IDS, k):
            rows = {i: [] for i in combo}; seed0 = 1000 * (len(tables) + 1)
            for rot in range(k):
                order = [combo[(j + rot) % k] for j in range(k)]
                for g in range(G):
                    out, _ = one_game(order, seed0 + rot * G + g)
                    for seat, who in enumerate(order):
                        rows[who].append(out[seat]); by_p[who].append(out[seat]); by_seat[who].setdefault((k, seat), []).append(out[seat])
            tables[combo] = rows
    metrics_of = lambda who, rows: {**S.game_metrics(playtest, words, PERSONAS[who]["preferred_minutes"], BRIEF), **S.bot_metrics(agg(rows))}
    fun_at = lambda who, rows: S.fun_from_metrics(metrics_of(who, rows), PERSONAS[who]["weights"])
    personas, matchups = {}, []
    for combo, rows in tables.items():
        if len(combo) == 2:
            a, b = combo; ra, rb = agg(rows[a]), agg(rows[b])
            matchups.append({"a": a, "b": b, "games": len(rows[a]), "a_win_rate": round(ra["win_rate"], 3), "note": "", "a_raw": ra, "b_raw": rb})
    os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
    for who in IDS:
        opts = [(fun_at(who, t[who]), c) for c, t in tables.items() if who in t]
        best, worst = max(opts), min(opts); raw = agg(by_p[who])
        seatw = {}
        for k in (2, 3, 4):
            for s in range(k):
                seatw["%dp seat %d" % (k, s + 1)] = round(agg(by_seat[who][(k, s)])["win_rate"], 3)
        personas[who] = {"raw": raw, "best_table": list(best[1]), "worst_table": list(worst[1]),
                         "bot": {"win_rate": round(raw["win_rate"], 3), "fell_behind_rate": round(raw["fell_behind_rate"], 3),
                                 "decisions_per_turn": round(raw["decisions_per_turn"], 2), "downtime": round(raw["downtime"], 2), "games": raw["games"],
                                 "seat_win_rates": seatw}}
        for n_, (_, combo) in enumerate((best, worst), 1):
            order = [who] + [c for c in combo if c != who]
            _, st = one_game(order, 777 + n_, log=True)
            with open(os.path.join(HERE, "logs", "%s-%d.txt" % (who, n_)), "w") as f:
                f.write("Fifty-Two Workshop: %s (seat 1) with %s, %s table for %s. Cards: rank+suit (S Spring, C Gear, D Jewel, H Clock face).\n"
                        % (who, ", ".join(order[1:]), "best" if n_ == 1 else "worst", who))
                f.write("\n".join(st.log[:60]) + "\n")
    out = {"personas": personas, "matchups": matchups,
           "rotation": {"player_counts": [2, 3, 4], "tables": len(tables), "seatings_per_table": "player count (cyclic rotation)",
                        "games_per_seating": G, "filler_bots": [], "note": "6 personas, so no filler bots; solo not included; seat win rates per table size in bot.seat_win_rates"}}
    json.dump(out, open(os.path.join(HERE, "panel-results.json"), "w"), indent=1); open(os.path.join(HERE, "panel-results.json"), "a").write("\n")
    print("rotation: %d tables, %d games per seating; games per persona: %s" % (len(tables), G, ", ".join("%s %d" % (i, len(by_p[i])) for i in IDS)))

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 200)
