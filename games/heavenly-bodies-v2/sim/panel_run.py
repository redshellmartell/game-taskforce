"""Panel rotation for Heavenly Bodies v2 at 2, 3 and 4 players. Every combination of personas per count, seats rotated cyclically.
Usage: python3 panel_run.py [games_per_seating=60]. Needs ../playtest.json. Writes panel-results.json and logs/<persona>-{1,2}.txt."""
import itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "panel"))
from multiprocessing import Pool
from game import play, cs, orb_str
import bots as B
import scoring as S

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SLUG = "heavenly-bodies-v2"
PERSONAS = S.load_personas(ROOT)
FIRST = ["casual", "competitor", "family", "story", "strategist"]
IDS = FIRST + sorted(set(PERSONAS) - set(FIRST))
BRIEF = json.load(open(os.path.join(ROOT, "games", SLUG, "brief.json")))


def one_game(order, seed, log=False):
    k = len(order)
    bots = [B.PERSONA[o](seed + 3 * s) for s, o in enumerate(order)]
    r = play(bots, seed, k, log=log); st = r["st"]; L = r["leaders"]; w = r["winner"]
    nz = [x for x in L if x is not None]; lc = sum(1 for x, y in zip(nz, nz[1:]) if x != y)
    mid = L[len(L) // 2] if L else None
    dec = st.stats["decisions"]; turns = r["turns"] or 1
    inter = st.stats["captures"] + st.stats["ties"]
    rows = []
    for seat in range(k):
        trailed = mid is not None and mid != seat
        rows.append(dict(won=int(w == seat), turns=turns, decisions=dec[seat], lead_changes=lc, trailed=int(trailed),
                         comeback=int(trailed and w == seat), inter=inter, opp_decisions=sum(dec) - dec[seat], mine_turns=turns / k))
    return rows, st


def task(a):
    tab, rot, g, seed = a
    order = tab[rot:] + tab[:rot]
    rows, _ = one_game(order, seed)
    return tab, order, rows


def agg(rows):
    n = len(rows); t = sum(r["mine_turns"] for r in rows) or 1; tr = sum(r["trailed"] for r in rows)
    return {"games": n, "win_rate": sum(r["won"] for r in rows) / n,
            "decisions_per_turn": sum(r["decisions"] for r in rows) / t,
            "lead_changes": sum(r["lead_changes"] for r in rows) / n,
            "comeback_rate": (sum(r["comeback"] for r in rows) / tr) if tr else 0.0,
            "fell_behind_rate": sum(1 for r in rows if r["trailed"] and not r["won"]) / n,
            "interaction_rate": sum(r["inter"] for r in rows) / (sum(r["turns"] for r in rows) or 1),
            "downtime": sum(r["opp_decisions"] for r in rows) / t}


def main(G=60):
    playtest = json.load(open(os.path.join(ROOT, "games", SLUG, "playtest.json")))
    words = len(open(os.path.join(ROOT, "games", SLUG, "rules.md"), encoding="utf-8").read().split())
    tasks = []; tables = []
    for k in (2, 3, 4):
        for ti, tab in enumerate(itertools.combinations(IDS, k)):
            tables.append(tab)
            for rot in range(k):
                for g in range(G):
                    tasks.append((tab, rot, g, 100000 * k + 1000 * ti + 50 * rot + g))
    with Pool(4) as pool:
        out = pool.map(task, tasks, chunksize=6)
    by_p = {i: [] for i in IDS}; by_seat = {i: {} for i in IDS}; by_table = {}
    for tab, order, rows in out:
        for seat, who in enumerate(order):
            by_p[who].append(rows[seat]); by_seat[who].setdefault((len(order), seat), []).append(rows[seat])
            by_table.setdefault((tab, who), []).append(rows[seat])
    metrics_of = lambda who, rows: {**S.game_metrics(playtest, words, PERSONAS[who]["preferred_minutes"], BRIEF), **S.bot_metrics(agg(rows))}
    fun_at = lambda who, rows: S.fun_from_metrics(metrics_of(who, rows), PERSONAS[who]["weights"])
    personas, matchups = {}, []
    for tab in [t for t in tables if len(t) == 2]:
        a, b = tab; ra, rb = agg(by_table[(tab, a)]), agg(by_table[(tab, b)])
        matchups.append({"a": a, "b": b, "games": len(by_table[(tab, a)]), "a_win_rate": round(ra["win_rate"], 3), "note": "", "a_raw": ra, "b_raw": rb})
    os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
    for who in IDS:
        opts = sorted([(fun_at(who, by_table[(t, who)]), t) for t in tables if who in t])
        worst, best = opts[0], opts[-1]
        raw = agg(by_p[who])
        seatwr = {}
        for (k, seat), rows in sorted(by_seat[who].items()):
            seatwr["%dp-seat%d" % (k, seat + 1)] = round(agg(rows)["win_rate"], 3)
        personas[who] = {"raw": raw, "best_table": list(best[1]), "worst_table": list(worst[1]),
                         "bot": {"win_rate": round(raw["win_rate"], 3), "fell_behind_rate": round(raw["fell_behind_rate"], 3),
                                 "decisions_per_turn": round(raw["decisions_per_turn"], 2), "downtime": round(raw["downtime"], 2),
                                 "games": raw["games"], "seat_win_rates": seatwr}}
        for n_, (_, tab) in enumerate((best, worst), 1):
            order = list(tab[tab.index(who):] + tab[:tab.index(who)])
            _, st = one_game(order, 777 + n_, log=True)
            with open(os.path.join(HERE, "logs", "%s-%d.txt" % (who, n_)), "w") as f:
                f.write("Heavenly Bodies v2: seats %s, table '%s' for %s. Cards: colour letter (E,F,V,S) + Size; [North East South West].\n"
                        % (", ".join(order), "best" if n_ == 1 else "worst", who))
                f.write("\n".join(st.log[:40]) + "\n")
    res = {"personas": personas, "matchups": matchups,
           "rotation": {"player_counts": [2, 3, 4], "tables": len(tables), "seatings_per_table": "k (cyclic rotation)",
                        "games_per_seating": G, "filler_bots": []}}
    json.dump(res, open(os.path.join(HERE, "panel-results.json"), "w"), indent=1)
    print("panel rotation: %d tables, %d games per seating, %s" % (len(tables), G, ", ".join("%s %d" % (i, len(by_p[i])) for i in IDS)))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 60)
