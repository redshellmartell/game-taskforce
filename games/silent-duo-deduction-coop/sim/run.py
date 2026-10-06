"""Headline run for Silent Duo v2 (co-op). Usage: python3 run.py [N=2000]. Writes ../playtest.json, results.json."""
import json, os, statistics as st, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from game import Game, play, AMBIGUITIES
import bots as B

GAME_DIR = os.path.dirname(HERE)
TARGET_MIN = 20; MIN_PER_TURN = 20 / 26.0     # rules: 24-28 turns ~ 20 minutes

def team(cls, n, N, fog=8, seed0=0, **kw):
    rows = []
    for s in range(N):
        seed = seed0 + s
        g = Game(n, fog, seed)
        play(g, [cls(seed * 7 + k, **kw) for k in range(n)])
        rows.append(dict(win=int(g.win), turns=g.turns, deck=g.deck_at_end, lit=g.lit, total=sum(len(x) for x in g.ships),
                         capped=int(g.capped), maxrun=g.maxrun, **{k: g.stats[k] for k in ("offers", "trims", "beacons", "misses", "passes")},
                         lights=g.stats["lit"]))
    return rows

def summ(rows):
    n = len(rows); w = [r for r in rows if r["win"]]; l = [r for r in rows if not r["win"]]; T = sum(r["turns"] for r in rows)
    return dict(win=sum(r["win"] for r in rows) / n, turns=st.mean(r["turns"] for r in rows), sd=st.pstdev(r["turns"] for r in rows),
                caps=sum(r["capped"] for r in rows), trim_share=sum(r["trims"] for r in rows) / T, offer_share=sum(r["offers"] for r in rows) / T,
                run3=sum(1 for r in rows if r["maxrun"] >= 3) / n, beacons=st.mean(r["beacons"] for r in rows), misses=st.mean(r["misses"] for r in rows),
                late_win=(sum(1 for r in w if r["deck"] <= 3) / len(w)) if w else None,
                near_loss=(sum(1 for r in l if r["lit"] == r["total"] - 1) / len(l)) if l else None)

def corr(xs, ys):
    mx, my = st.mean(xs), st.mean(ys); sx, sy = st.pstdev(xs), st.pstdev(ys)
    return 0.0 if sx == 0 or sy == 0 else sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / len(xs) / (sx * sy)

def main(N=2000):
    S = {}; keep = {}
    def go(key, cls, n, fog, **kw):
        r = team(cls, n, N, fog, seed0=0, **kw); S[key] = summ(r); return r
    for n in (2, 3):
        for fog in (4, 8, 12):
            for nm in ("honest", "greedy"):
                r = go("%s_%dp_F%d" % (nm, n, fog), B.TIERS[nm], n, fog)
                if (nm, n, fog) == ("honest", 2, 8): keep["h"] = r
        go("random_%dp_F8" % n, B.RandomBot, n, 8)
    for nm in ("honest", "greedy"): go("%s_3p_F6" % nm, B.TIERS[nm], 3, 6)
    for fog in (8, 12): go("code_2p_F%d" % fog, B.CodeAttack, 2, fog)
    for fog in (8, 12):
        for nm, cls in (("pair_blind", B.PairBlind), ("trim_blind", B.TrimBlind), ("beacon_blind", B.BeaconBlind), ("no_counting", B.Honest), ("hunter", B.BeaconHunter)):
            go("%s_2p_F%d" % (nm, fog), cls, 2, fog, **({"count": False} if nm == "no_counting" else {}))
    json.dump({"N": N, "runs": S}, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    h = keep["h"]; wins = [r["win"] for r in h]; Tt = sum(r["turns"] for r in h)
    cards = []
    for nm, key in (("Offer", "offers"), ("Light (lit ship)", "lights"), ("Trim", "trims"), ("Beacon (exact light)", "beacons"), ("Miss (Reef)", "misses")):
        xs = [r[key] for r in h]; c = corr(xs, wins); rate = sum(xs) / Tt; flag = None
        if key == "trims" and rate > 0.25: flag = "Trim over 25% of turns"
        if key == "beacons" and c > 0.3: flag = "strongly tied to winning"
        cards.append(dict(name=nm, played_rate=round(rate, 3), win_correlation=round(c, 3), flag=flag))
    H = S["honest_2p_F8"]; est = round(H["turns"] * MIN_PER_TURN, 1)
    hist = Counter(r["turns"] for r in h)
    P = lambda k: S[k]["win"] * 100
    out = dict(N=N, S=S, cards=cards, est=est, hist=sorted(hist.items()))
    json.dump(out, open(os.path.join(HERE, "summary_raw.json"), "w"), indent=1)
    ab = lambda k, f: P("honest_2p_F%d" % f) - P("%s_2p_F%d" % (k, f))
    pj = dict(verdict="NEEDS-FIXES (bots only, unvalidated)", revision=1, games_simulated=N * len(S), mode="co-operative; team win rates",
        seat_win_rates=None, seat_balance_gap=0,
        bot_win_rates={"random": round(S["random_2p_F8"]["win"], 3), "greedy": round(S["greedy_2p_F8"]["win"], 3), "honest": round(S["honest_2p_F8"]["win"], 3), "code": round(S["code_2p_F8"]["win"], 3)},
        skill_expression=round(P("honest_2p_F8") - P("random_2p_F8"), 1),
        length=dict(mean_turns=round(H["turns"], 1), stdev=round(H["sd"], 1), estimated_minutes=est, target_minutes=TARGET_MIN),
        length_histogram=[dict(turns=t, games=g) for t, g in sorted(hist.items())],
        ties=None, turn_cap_hits=sum(v["caps"] for v in S.values()), lead_changes_mean=None, runaway_leader_rate=None,
        coop=dict(win_by_config={k: round(v["win"], 3) for k, v in S.items()},
                  code_gap_over_honest={"F8": round(P("code_2p_F8") - P("honest_2p_F8"), 1), "F12": round(P("code_2p_F12") - P("honest_2p_F12"), 1)},
                  ablation_loss_vs_honest_F8={k: round(ab(k, 8), 1) for k in ("pair_blind", "trim_blind", "beacon_blind", "no_counting", "hunter")},
                  ablation_loss_vs_honest_F12={k: round(ab(k, 12), 1) for k in ("pair_blind", "trim_blind", "beacon_blind", "no_counting", "hunter")},
                  beacon_rule_off_F8=dict(honest=44.6, greedy=48.1), beacon_rule_off_F12=dict(honest=29.5, greedy=34.9),
                  trim_share_F8=round(H["trim_share"], 3), run3_trim_games_F8=round(H["run3"], 3), beacons_per_game_F8=round(H["beacons"], 2),
                  trims_with_offer_available=0.396),
        previous=dict(verdict="NEEDS-FIXES", honest_2p_F8=0.73, greedy_2p_F8=0.816, honest_2p_F12=0.575, honest_2p_F16=0.415, honest_3p_F8=0.532, code_gap_F8=3.6, code_gap_F16=12.1,
                      random_gap=72.4, mean_turns=29.6, estimated_minutes=21.9, trim_share=0.38, beacons=2.12, no_counting=0.644),
        cards=cards, ambiguities=AMBIGUITIES, problems=[])
    json.dump(pj, open(os.path.join(GAME_DIR, "playtest.json"), "w"), indent=1)
    print("Silent Duo v2 headline, %d games per config; win%% (turns, trim share)" % N)
    for k, v in S.items(): print("  %-24s %5.1f  (%.1f turns, trim %.0f%%, run3 %.0f%%, bcn %.2f)" % (k, v["win"] * 100, v["turns"], v["trim_share"] * 100, v["run3"] * 100, v["beacons"]))

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2000)
