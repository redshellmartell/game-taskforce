"""Panel rotation for Whiskerdark (solo): each persona plays alone, 1,000 runs on random layouts (no Ghosts).
competitor and barraiser use the slow lookahead bot, so they play 300 runs. Writes panel-results.json and logs/<persona>-1/2.txt.
Solo proxies (read the report): lead_changes = swings of the Ready count between <=1 and >=3; comeback = win rate when
Ready <=1 at the run's halfway turn; interaction and downtime are 0 (no opponent).
Usage: python3 panel_run.py [runs=1000]"""
import json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "panel"))
from game import play
import bots as B
import scoring as S
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PERSONAS = S.load_personas(ROOT)
IDS = ["casual", "competitor", "family", "story", "strategist", "barraiser"]
SLOW = {"competitor": lambda s: B.Lookahead(s, K=6), "barraiser": lambda s: B.Lookahead(s, K=12)}

def one(who, seed, log=False):
    rng = random.Random(seed); pm = list(range(1, 10)); rng.shuffle(pm)
    bot = SLOW[who](seed) if who in SLOW else B.PERSONA[who](seed)
    r = play(pm, (), bot, log=log); t = r.stats["ready_traj"]
    mid = t[len(t) // 2] if t else 0
    state = None; swings = 0
    for x in t:
        s = "low" if x <= 1 else "high" if x >= 3 else None
        if s and state and s != state: swings += 1
        if s: state = s
    return r, dict(won=int(r.won), turns=r.turns, decisions=r.decisions, lead_changes=swings, trailed=int(mid <= 1 and len(t) >= 3),
                   comeback=int(mid <= 1 and len(t) >= 3 and r.won), busts=0, bait=0, opp_decisions=0)

def agg(rows):
    n = len(rows); t = sum(r["turns"] for r in rows) or 1; tr = sum(r["trailed"] for r in rows)
    return {"games": n, "win_rate": sum(r["won"] for r in rows) / n, "decisions_per_turn": sum(r["decisions"] for r in rows) / t,
            "lead_changes": sum(r["lead_changes"] for r in rows) / n,
            "comeback_rate": (sum(r["comeback"] for r in rows) / tr) if tr else 0.0,
            "fell_behind_rate": sum(1 for r in rows if r["trailed"] and not r["won"]) / n,
            "interaction_rate": 0.0, "downtime": 0.0}

def main(runs=1000):
    os.makedirs(os.path.join(HERE, "logs"), exist_ok=True); personas = {}
    for k, who in enumerate(IDS):
        n = 300 if who in SLOW else runs; rows = []; won_seed = lost_seed = None
        for i in range(n):
            seed = 100000 * (k + 1) + i; r, row = one(who, seed); rows.append(row)
            if r.won and won_seed is None: won_seed = seed
            if not r.won and lost_seed is None: lost_seed = seed
        raw = agg(rows)
        personas[who] = {"raw": raw, "best_table": [who], "worst_table": [who],
                         "bot": {"win_rate": round(raw["win_rate"], 3), "fell_behind_rate": round(raw["fell_behind_rate"], 3),
                                 "decisions_per_turn": round(raw["decisions_per_turn"], 2), "downtime": 0.0, "games": n,
                                 "seat_win_rates": {"1": round(raw["win_rate"], 3)}}}
        for j, sd in enumerate((won_seed, lost_seed), 1):
            if sd is None: continue
            r, _ = one(who, sd, log=True)
            open(os.path.join(HERE, "logs", "%s-%d.txt" % (who, j)), "w").write(
                "Whiskerdark, solo, %s bot, seed %d (%s run). Solo game: one table per persona.\n" % (who, sd, "won" if j == 1 else "lost") + "\n".join(r.log) + "\n")
        print(who, "runs", n, "win %.3f" % raw["win_rate"], "dec/turn %.2f" % raw["decisions_per_turn"], flush=True)
    out = {"personas": personas, "matchups": [], "rotation": {"player_counts": [1], "tables": len(IDS), "seatings_per_table": 1,
           "games_per_seating": runs, "filler_bots": []}}
    json.dump(out, open(os.path.join(HERE, "panel-results.json"), "w"), indent=1)

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1000)
