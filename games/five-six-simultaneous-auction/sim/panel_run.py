"""Panel rotation for Last Bid Standing. Tables = every combination of personas at 5 players (6 tables of 5 from 6 personas)
plus the single 6-player table; seats rotate cyclically (every persona in every seat equally often), 200 games per seating.
Writes sim/panel-results.json and sim/logs/<persona>-1.txt (best table) and -2.txt (worst table).
Usage: python3 panel_run.py [games_per_seating=200]"""
import itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "panel"))
from game import Config, play
import bots as B
import scoring as S

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SLUG = "five-six-simultaneous-auction"
PERSONAS = S.load_personas(ROOT)
IDS = sorted(PERSONAS)
BRIEF = json.load(open(os.path.join(ROOT, "games", SLUG, "brief.json")))

class Count:
    def __init__(self, bot): self.bot = bot; self.n = 0
    def __getattr__(self, k): return getattr(self.bot, k)
    def bid(self, st, p): self.n += 1; return self.bot.bid(st, p)
    def pick(self, st, p, lots): self.n += 1; return self.bot.pick(st, p, lots)

def one_game(seating, seed, log=False):
    cfg = Config(players=len(seating), log=log)
    bots = [Count(B.PERSONA[w](seed + i * 13)) for i, w in enumerate(seating)]
    r = play(cfg, bots, seed); st = r["st"]; w = r["winners"]; n = len(seating)
    nz = [l for l in st.leaders if l >= 0]; lc = sum(1 for a, b in zip(nz, nz[1:]) if a != b)
    half = st.score_hist[cfg.rounds // 2 - 1]; top = max(half)
    out = []
    for i, c in enumerate(bots):
        trailed = top - half[i] >= 3                       # at least 3 points behind the halfway leader
        won = int(i in w) / len(w)
        out.append(dict(won=won, turns=cfg.rounds, decisions=c.n, lead_changes=lc, trailed=int(trailed),
                        comeback=int(trailed and i in w), interaction=st.cancelled_by[i],
                        opp_decisions=sum(b.n for j, b in enumerate(bots) if j != i)))
    return out, st

def agg(rows):
    n = len(rows); t = sum(r["turns"] for r in rows) or 1; tr = sum(r["trailed"] for r in rows)
    return {"games": n, "win_rate": sum(r["won"] for r in rows) / n,
            "decisions_per_turn": sum(r["decisions"] for r in rows) / t,
            "lead_changes": sum(r["lead_changes"] for r in rows) / n,
            "comeback_rate": (sum(r["comeback"] for r in rows) / tr) if tr else 0.0,
            "fell_behind_rate": sum(1 for r in rows if r["trailed"] and not r["won"]) / n,
            "interaction_rate": sum(r["interaction"] for r in rows) / t,
            # simultaneous bidding: nobody waits on a turn; the only wait is the first bidder picking a lot (1 pick per round)
            "downtime": 1.0}

def main(per=200):
    playtest = json.load(open(os.path.join(ROOT, "games", SLUG, "playtest.json")))
    words = len(open(os.path.join(ROOT, "games", SLUG, "rules.md"), encoding="utf-8").read().split())
    by_p = {i: [] for i in IDS}; by_seat = {i: {} for i in IDS}; tables = {}; seat_rows = {}
    combos = [c for k in (5, 6) for c in itertools.combinations(IDS, k)]
    for ti, combo in enumerate(combos):
        n = len(combo); rows = {w: [] for w in combo}
        for rot in range(n):
            seating = list(combo[rot:] + combo[:rot])
            for k in range(per):
                out, _ = one_game(seating, 5000000 + ti * 100000 + rot * 1000 + k)
                for seat, w in enumerate(seating):
                    rows[w].append((seat, out[seat])); by_p[w].append(out[seat]); by_seat[w].setdefault(seat, []).append(out[seat])
        tables[combo] = rows
    metrics_of = lambda who, rows: {**S.game_metrics(playtest, words, PERSONAS[who]["preferred_minutes"], BRIEF), **S.bot_metrics(agg(rows))}
    fun_at = lambda who, rows: S.fun_from_metrics(metrics_of(who, rows), PERSONAS[who]["weights"])
    personas, matchups = {}, []
    os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
    for who in IDS:
        opts = [(fun_at(who, [r for _, r in rows[who]]), combo) for combo, rows in tables.items() if who in rows]
        best, worst = max(opts), min(opts)
        raw = agg(by_p[who])
        sw = {str(s + 1): round(agg(v)["win_rate"], 3) for s, v in sorted(by_seat[who].items())}
        personas[who] = {"raw": raw, "best_table": list(best[1]), "worst_table": list(worst[1]),
                         "bot": {"win_rate": round(raw["win_rate"], 3), "fell_behind_rate": round(raw["fell_behind_rate"], 3),
                                 "decisions_per_turn": round(raw["decisions_per_turn"], 2), "downtime": round(raw["downtime"], 2),
                                 "games": raw["games"], "seat_win_rates": sw}}
        for nlog, (_, combo) in enumerate((best, worst), 1):
            seating = list(combo[combo.index(who):] + combo[:combo.index(who)])
            _, st = one_game(seating, 777 + nlog, log=True)
            with open(os.path.join(HERE, "logs", "%s-%d.txt" % (who, nlog)), "w") as f:
                f.write("Last Bid Standing: %s sits seat 1; table %s ('%s' table for %s). Cards are (category 0-3, value).\n"
                        % (who, ", ".join(seating), "best" if nlog == 1 else "worst", who))
                f.write("\n".join(st.log) + "\nFinal Hype %s\n" % st.hype_counts())
    for a, b in itertools.combinations(IDS, 2):
        ra, rb = [], []
        for combo, rows in tables.items():
            if a in rows and b in rows:
                ra += [r for _, r in rows[a]]; rb += [r for _, r in rows[b]]
        A, Bq = agg(ra), agg(rb)
        matchups.append({"a": a, "b": b, "games": len(ra), "a_win_rate": round(A["win_rate"], 3),
                         "note": "games at tables containing both; win rates are per-player shares", "a_raw": A, "b_raw": Bq})
    out = {"personas": personas, "matchups": matchups,
           "rotation": {"player_counts": [5, 6], "tables": len(tables), "seatings_per_table": "5 (5p tables) / 6 (6p table), cyclic",
                        "games_per_seating": per, "filler_bots": [],
                        "note": "6 personas incl. barraiser: 6 tables of 5 and 1 table of 6; no filler bots needed"}}
    with open(os.path.join(HERE, "panel-results.json"), "w") as f:
        json.dump(out, f, indent=1); f.write("\n")
    print("rotation: %d tables, %d games per persona (%s)" % (len(tables), len(by_p[IDS[0]]), ", ".join("%s %d" % (i, len(by_p[i])) for i in IDS)))

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 200)
