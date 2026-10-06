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
                         capped=int(g.capped), maxrun=g.maxrun, **{k: g.stats[k] for k in ("offers", "trims", "beacons", "misses", "passes", "singles", "trims_total", "trims_with_offer")},
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
        r = team(cls, n, N, fog, seed0=0, **kw); S[key] = summ(r); S[key]["trims_with_offer"] = sum(x["trims_with_offer"] for x in r) / max(1, sum(x["trims_total"] for x in r)); S[key]["single_share"] = sum(x["singles"] for x in r) / sum(x["turns"] for x in r); return r
    TW = [0]
    ST = {2: 6, 3: 2}
    for n, fogs in ((2, (3, 6, 10)), (3, (0, 2, 6))):
        for fog in fogs:
            for nm in ("honest", "greedy"):
                r = go("%s_%dp_F%d" % (nm, n, fog), B.TIERS[nm], n, fog)
                if (nm, n, fog) == ("honest", 2, 6): keep["h"] = r
                if (nm, n, fog) == ("honest", 3, 2): keep["h3"] = r
        go("random_%dp_F%d" % (n, ST[n]), B.RandomBot, n, ST[n])
    for fog in (6, 10): go("code_2p_F%d" % fog, B.CodeAttack, 2, fog)
    for n in (2, 3):
        for nm, cls in (("pair_blind", B.PairBlind), ("trim_blind", B.TrimBlind), ("no_counting", B.Honest), ("single_blind", B.SingleBlind)):
            go("%s_%dp_F%d" % (nm, n, ST[n]), cls, n, ST[n], **({"count": False} if nm == "no_counting" else {}))
    json.dump({"N": N, "runs": S}, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    h = keep["h"]; wins = [r["win"] for r in h]; Tt = sum(r["turns"] for r in h)
    cards = []
    for nm, key in (("Pair Offer", "offers"), ("Single Offer", "singles"), ("Light (lit ship)", "lights"), ("Trim", "trims"), ("Miss (Reef)", "misses")):
        xs = [r[key] - (r["singles"] if key == "offers" else 0) for r in h]; c = corr(xs, wins); rate = sum(xs) / Tt; flag = None
        if key == "trims" and rate > 0.25: flag = "Trim over 25% of turns"
        cards.append(dict(name=nm, played_rate=round(rate, 3), win_correlation=round(c, 3), flag=flag))
    H = S["honest_2p_F6"]; est = round(H["turns"] * MIN_PER_TURN, 1)
    hist = Counter(r["turns"] for r in h)
    P = lambda k: S[k]["win"] * 100
    ab = lambda k, n: P("honest_%dp_F%d" % (n, ST[n])) - P("%s_%dp_F%d" % (k, n, ST[n]))
    prev = json.load(open(os.path.join(GAME_DIR, "playtest.json")))
    prev_small = dict(verdict=prev["verdict"], revision=prev["revision"], mean_turns=prev["length"]["mean_turns"], coop=prev["coop"]["win_by_config"],
                      ablation_F8=prev["coop"]["ablation_loss_vs_honest_F8"], code_gap_F8=prev["coop"]["code_gap_over_honest"]["F8"],
                      trim_share=prev["coop"]["trim_share_F8"], run3=prev["coop"]["run3_trim_games_F8"], skill_expression=prev["skill_expression"])
    json.dump(dict(N=N, S=S), open(os.path.join(HERE, "summary_raw.json"), "w"), indent=1)
    pj = dict(verdict="NEEDS-FIXES (bots only, unvalidated)", revision=2, games_simulated=N * len(S), mode="co-operative; team win rates",
        seat_win_rates=None, seat_balance_gap=0,
        bot_win_rates={"random": round(S["random_2p_F6"]["win"], 3), "greedy": round(S["greedy_2p_F6"]["win"], 3), "honest": round(S["honest_2p_F6"]["win"], 3), "code": round(S["code_2p_F6"]["win"], 3)},
        skill_expression=round(P("honest_2p_F6") - P("random_2p_F6"), 1),
        length=dict(mean_turns=round(H["turns"], 1), stdev=round(H["sd"], 1), estimated_minutes=est, target_minutes=TARGET_MIN),
        length_histogram=[dict(turns=t, games=g) for t, g in sorted(hist.items())],
        ties=None, turn_cap_hits=sum(v["caps"] for v in S.values()), lead_changes_mean=None, runaway_leader_rate=None,
        coop=dict(win_by_config={k: round(v["win"], 3) for k, v in S.items()},
                  code_gap_over_honest={"F6": round(P("code_2p_F6") - P("honest_2p_F6"), 1), "F10": round(P("code_2p_F10") - P("honest_2p_F10"), 1)},
                  ablation_loss_vs_honest_2p={k: round(ab(k, 2), 1) for k in ("pair_blind", "trim_blind", "no_counting", "single_blind")},
                  ablation_loss_vs_honest_3p={k: round(ab(k, 3), 1) for k in ("pair_blind", "trim_blind", "no_counting", "single_blind")},
                  trim_share_2p=round(H["trim_share"], 3), run3_2p=round(H["run3"], 3), trim_share_3p=round(S["honest_3p_F2"]["trim_share"], 3), run3_3p=round(S["honest_3p_F2"]["run3"], 3),
                  greedy_minus_honest_3p_F2=round(P("greedy_3p_F2") - P("honest_3p_F2"), 1), greedy_minus_honest_2p_F6=round(P("greedy_2p_F6") - P("honest_2p_F6"), 1),
                  mean_turns_3p_F2=round(S["honest_3p_F2"]["turns"], 1)),
        previous=prev_small, cards=cards, ambiguities=AMBIGUITIES, problems=[])
    json.dump(pj, open(os.path.join(GAME_DIR, "playtest.json"), "w"), indent=1)
    print("Silent Duo v3 headline, %d games per config; win%% (turns, trim share, run3, trims-with-offer)" % N)
    for k, v in S.items(): print("  %-22s %5.1f  (%.1f t, trim %.0f%%, run3 %.0f%%, caps %d)" % (k, v["win"] * 100, v["turns"], v["trim_share"] * 100, v["run3"] * 100, v["caps"]))

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2000)
