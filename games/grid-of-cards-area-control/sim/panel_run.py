"""Panel rotation for Nine Fields: every combination of personas at 2, 3 and 4 players, seats rotated cyclically,
same games per persona in every seat. Writes sim/panel-results.json and sim/logs/<persona>-1/2.txt.
Usage: python3 panel_run.py [games_per_seating=200]"""
import itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "panel"))
import game as G, bots as B, scoring as S
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SLUG = "grid-of-cards-area-control"
PERSONAS = S.load_personas(ROOT)
IDS = ["casual", "competitor", "family", "story", "strategist", "barraiser"]
BRIEF = json.load(open(os.path.join(ROOT, "games", SLUG, "brief.json")))
COUNTS = (2, 3, 4)

def one_game(table, seed, log=False):
    n = len(table)
    bs = [B.PERSONA[w](seed * 13 + i) for i, w in enumerate(table)]
    r = G.play(n, bs, seed, log=log); st = r["st"]
    seq = [x for x in r["leads"] if x >= 0]
    lc = sum(1 for a, b in zip(seq, seq[1:]) if a != b)
    mid = r["mid"]; own_turns = r["turns"] / n; out = []
    for seat in range(n):
        trailed = mid is not None and mid >= 0 and mid != seat
        out.append(dict(won=r["w"][seat], turns=own_turns, decisions=st.dec[seat], lead_changes=lc,
                        trailed=int(trailed), comeback=(r["w"][seat] if trailed else 0),
                        inter=st.inter[seat], opp_decisions=sum(st.dec) - st.dec[seat]))
    return out, st

def agg(rows):
    n = len(rows); t = sum(r["turns"] for r in rows) or 1; tr = sum(r["trailed"] for r in rows)
    return {"games": n, "win_rate": sum(r["won"] for r in rows) / n, "decisions_per_turn": sum(r["decisions"] for r in rows) / t,
            "lead_changes": sum(r["lead_changes"] for r in rows) / n,
            "comeback_rate": (sum(r["comeback"] for r in rows) / tr) if tr else 0.0,
            "fell_behind_rate": sum(1 for r in rows if r["trailed"] and not r["won"]) / n,
            "interaction_rate": sum(r["inter"] for r in rows) / t, "downtime": sum(r["opp_decisions"] for r in rows) / t}

def main(per=200):
    playtest = json.load(open(os.path.join(ROOT, "games", SLUG, "playtest.json")))
    words = len(open(os.path.join(ROOT, "games", SLUG, "rules.md"), encoding="utf-8").read().split())
    by_p = {i: [] for i in IDS}; by_seat3 = {i: {0: [], 1: [], 2: []} for i in IDS}
    tables = {}
    for n in COUNTS:
        for combo in itertools.combinations(IDS, n):
            rows = {w: [] for w in combo}; base = 1000 * (COUNTS.index(n) * 100 + IDS.index(combo[0]) * 20 + sum(IDS.index(c) for c in combo))
            for rot in range(n):                                  # cyclic seating: each persona sits in each seat equally often
                table = [combo[(i + rot) % n] for i in range(n)]
                for k in range(per):
                    out, _ = one_game(table, base + rot * per + k)
                    for seat, who in enumerate(table):
                        rows[who].append(out[seat]); by_p[who].append(out[seat])
                        if n == 3: by_seat3[who][seat].append(out[seat])
            tables[combo] = rows
    metrics_of = lambda who, rows: {**S.game_metrics(playtest, words, PERSONAS[who]["preferred_minutes"], BRIEF), **S.bot_metrics(agg(rows))}
    fun_at = lambda who, rows: S.fun_from_metrics(metrics_of(who, rows), PERSONAS[who]["weights"])
    personas, matchups = {}, []
    for combo, rows in tables.items():
        if len(combo) == 2:
            a, b = combo; ra, rb = agg(rows[a]), agg(rows[b])
            matchups.append({"a": a, "b": b, "games": len(rows[a]), "a_win_rate": round(ra["win_rate"], 3), "note": "", "a_raw": ra, "b_raw": rb})
    for who in IDS:
        opts = [(fun_at(who, rows[who]), combo) for combo, rows in tables.items() if who in rows]
        best, worst = max(opts), min(opts); raw = agg(by_p[who])
        personas[who] = {"raw": raw, "best_table": list(best[1]), "worst_table": list(worst[1]),
            "bot": {"win_rate": round(raw["win_rate"], 3), "fell_behind_rate": round(raw["fell_behind_rate"], 3),
                    "decisions_per_turn": round(raw["decisions_per_turn"], 2), "downtime": round(raw["downtime"], 2), "games": raw["games"],
                    "seat_win_rates": {str(s + 1): round(agg(by_seat3[who][s])["win_rate"], 3) for s in range(3)}}}
        os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
        for n_, (_, combo) in enumerate((best, worst), 1):
            table = list(combo)
            if who in table: table.remove(who)
            table = [who] + table
            _, st = one_game(table, 777 + n_, log=True)
            with open(os.path.join(HERE, "logs", "%s-%d.txt" % (who, n_)), "w") as f:
                f.write("Nine Fields: seats 1.. = %s; %s table for %s. Cells 0-8 in reading order; scores are trophy totals.\n" % (", ".join(table), "best" if n_ == 1 else "worst", who))
                f.write("\n".join(st.log[:40]) + "\n")
    out = {"personas": personas, "matchups": matchups,
           "rotation": {"player_counts": list(COUNTS), "main_player_count": 3, "tables": len(tables), "seatings_per_table": "N (cyclic, one per seat)",
                        "games_per_seating": per, "filler_bots": [],
                        "note": "6 personas, so every table up to 4 players is filled by personas: no filler bots. Seat win rates in persona entries are from the 3-player tables."}}
    json.dump(out, open(os.path.join(HERE, "panel-results.json"), "w"), indent=1); 
    print("rotation: %d tables, %d games per persona" % (len(tables), len(by_p[IDS[0]])))
if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 200)
