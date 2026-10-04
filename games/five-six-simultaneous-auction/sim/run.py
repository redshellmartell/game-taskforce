"""Headline run + experiments for Last Bid Standing. Usage: python3 run.py [games=2000] [--no-exp]
Writes ../playtest.json (verdict fields filled by hand-reviewed constants below) and sim/results.json."""
import json, math, os, sys, statistics as stt
from dataclasses import replace
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from game import Config, play, CATS
import bots as B
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SLUG = "five-six-simultaneous-auction"
TARGET_MIN = 20

def table(kind, n, g):
    """bot class list for a table; rotated by game index g so every bot meets every seat equally."""
    S, R, G = B.Strategic, B.Random, B.Greedy
    base = {"mixed": [S, R, G, S, R, G], "SvR": [S, R, S, R, S, R], "allS": [S] * 6, "allR": [R] * 6, "allG": [G] * 6,
            "oneS": [S, R, R, R, R, R]}[kind][:n]
    k = g % n
    return base[k:] + base[:k]          # list index = seat; rotation shifts which seat each bot gets

def pearson(x, y):
    n = len(x); mx, my = sum(x) / n, sum(y) / n
    sx = math.sqrt(sum((a - mx) ** 2 for a in x)); sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy) if sx and sy else 0.0

def evaluate(cfg, kind, N, seed0=0, detail=False):
    n = cfg.players; seat = [0.0] * n; byb = {}; cnt = {}; ties = 0
    leadch = []; early = []; early10 = []; cap = 0
    unsold = canc = nodraw = resh = forced = 0; hype_pts = tot_pts = 0; lastflip = crashflip = 0
    handavg = []; leftover = []; sec = []; crashed = [0] * CATS; crash_none = 0; margin = []
    X = {"pass": [], "bid": [[] for _ in range(11)], "lotcat": [[] for _ in range(CATS)], "lotval": [[] for _ in range(6)],
         "win": [], "plays": [[0, 0] for _ in range(11)]}
    for g in range(N):
        classes = table(kind, n, g)
        bots = [c(seed0 + g * 7 + i) for i, c in enumerate(classes)]
        r = play(cfg, bots, seed0 + g); st = r["st"]; w = r["winners"]
        for x in w:
            seat[x] += 1 / len(w); byb.setdefault(classes[x].name, [0.0, 0]); byb[classes[x].name][0] += 1 / len(w)
        for c in classes: byb.setdefault(c.name, [0.0, 0]); byb[c.name][1] += 1
        ties += len(w) > 1
        lc = 0; last = -1
        for l in st.leaders:
            if l >= 0:
                if last >= 0 and l != last: lc += 1
                last = l
        leadch.append(lc)
        for arr, idx in ((early, cfg.rounds // 2), (early10, cfg.rounds - 3)):
            l = st.leaders[idx - 1]
            if l >= 0: arr.append(1 if l in w else 0)
        unsold += st.stats["unsold"]; canc += st.stats["cancelled"]; nodraw += st.stats["nodraw"]; resh += st.stats["reshuffles"]
        forced += st.stats["forced_pass"]; handavg.append(st.stats["hand_sum"] / st.stats["hand_obs"])
        leftover.append(sum(len(h) for h in st.hands) / n); sec.append(st.stats["sec"])
        sc, eff = r["scores"], r["eff"]
        hp = sum(eff[c] for p in range(n) for c, v in st.won[p]); hype_pts += hp; tot_pts += sum(sc)
        for c in st.crashed(): crashed[c] += 1
        if st.leader_before_last is not None and st.leader_before_last >= 0 and st.leader_before_last not in w: lastflip += 1
        if st.crash_before_last != st.crashed(): crashflip += 1
        ss = sorted(sc, reverse=True); margin.append(ss[0] - ss[1])
        if detail:
            for p in range(n):
                win = 1 if p in w else 0; X["win"].append(win)
                X["pass"].append(st.plays[p]["pass_"])
                for v in range(1, cfg.bid_max + 1): X["bid"][v].append(st.plays[p]["bid"][v])
                for c in range(CATS): X["lotcat"][c].append(sum(1 for l in st.won[p] if l[0] == c))
                for v in range(1, 6): X["lotval"][v].append(sum(1 for l in st.won[p] if l[1] - cfg.lot_bonus == v))
            for v in range(1, cfg.bid_max + 1):
                X["plays"][v][0] += sum(pl["bid"][v] for pl in st.plays); X["plays"][v][1] += st.lotwins_by_bid[v]
    res = dict(n=n, N=N, seat={i + 1: seat[i] / N for i in range(n)}, bot={k: v[0] / v[1] for k, v in byb.items()},
               ties=ties / N, lead_changes=sum(leadch) / N, runaway_half=sum(early) / max(1, len(early)),
               runaway_late=sum(early10) / max(1, len(early10)), unsold_per_game=unsold / N, cancelled_bids_per_game=canc / N,
               nodraw_per_game=nodraw / N, reshuffles=resh / N, forced_pass_rate=forced / (N * n * cfg.rounds),
               hype_share_of_points=hype_pts / max(1, tot_pts), mean_hand=sum(handavg) / N, leftover_cards=sum(leftover) / N,
               minutes=2 + 1 + sum(sec) / N / 60, minutes_sd=stt.pstdev(sec) / 60, last_round_winner_flip=lastflip / N,
               last_round_crash_flip=crashflip / N, crash_rate_by_cat=[c / N for c in crashed], mean_margin=sum(margin) / N,
               leadchange_hist=[leadch.count(k) for k in range(max(leadch) + 1)])
    if detail: res["X"] = X
    return res

def spread(res):  # max deviation of a seat from fair, in points
    return max(abs(v - 1 / res["n"]) for v in res["seat"].values()) * 100

def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 2000
    out = {"headline": {}, "experiments": {}}
    for n in (5, 6):
        cfg = Config(players=n)
        for kind in ("mixed", "SvR", "oneS", "allS", "allR", "allG"):
            out["headline"]["%dp-%s" % (n, kind)] = evaluate(cfg, kind, N, seed0=n * 100000, detail=(kind == "mixed"))
    # experiments (max 5), single change each, 6 players, 1000 games
    EXP = {
      "E1 lots+2": dict(lot_bonus=2), "E2 income2": dict(income=2), "E3 halve": dict(bubble="halve"),
      "E4 bid1-12": dict(bid_max=12), "E5 hand5": dict(start_hand=5),
    } if "--no-exp" not in sys.argv else {}
    for name, kw in EXP.items():
        for n in (6,):
            for kind in ("oneS", "allS"):
                out["experiments"]["%s %dp-%s" % (name, n, kind)] = evaluate(replace(Config(players=n), **kw), kind, N // 2, seed0=777000 + n)
    for k, v in out["headline"].items():
        v.pop("X", None) if k.endswith("mixed") and False else None
    write_playtest(out, N)
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(out, f, default=lambda o: o, indent=1)
    h = out["headline"]; line = lambda r: "seatgap %.1f | bots %s | LC %.2f | runaway %.2f/%.2f | min %.1f | tie %.3f" % (
        spread(r), {k: round(v * 100, 1) for k, v in r["bot"].items()}, r["lead_changes"], r["runaway_half"], r["runaway_late"], r["minutes"], r["ties"])
    pass
    out["headline"]["6p-allS"]  # baseline for comparison
    ex = lambda r: "unsold %.1f hype%% %.0f forced%% %.0f tie %.3f LC %.2f run %.2f/%.2f flip %.2f min %.1f bots %s seatgap %.1f" % (
        r["unsold_per_game"], r["hype_share_of_points"] * 100, r["forced_pass_rate"] * 100, r["ties"], r["lead_changes"], r["runaway_half"],
        r["runaway_late"], r["last_round_winner_flip"], r["minutes"], {k: round(v * 100, 1) for k, v in r["bot"].items()}, spread(r))
    print("--- baselines (6p) vs experiments (6p, %d games)" % (N // 2))
    for k in ("6p-oneS", "6p-allS"): print("BASE", k, ex(h[k]))
    for k, r in out["experiments"].items(): print(k, ex(r))

def write_playtest(out, N):
    h = out["headline"]; avg = lambda k, f: (f(h["5p-" + k]) + f(h["6p-" + k])) / 2
    m5, m6 = h["5p-mixed"], h["6p-mixed"]
    bw = {}
    for k in ("random", "greedy", "strategic"):
        bw[k] = round((m5["bot"][k] + m6["bot"][k]) / 2, 3)
    gap = lambda r: (r["bot"]["strategic"] - r["bot"]["random"]) * 100
    skill = round((gap(h["5p-oneS"]) + gap(h["6p-oneS"])) / 2, 1)
    X = m6["X"]; tot = lambda r: r["N"] * r["n"]
    cards = []
    def add(name, played, vals, flag=None):
        cards.append({"name": name, "played_rate": round(played, 3), "win_correlation": round(pearson(vals, X6["win"]), 3), "flag": flag})
    X6 = m6["X"]
    cards.append({"name": "Pass (Paddle)", "played_rate": round(sum(X6["pass"]) / (len(X6["win"]) * 14), 3), "win_correlation": round(pearson(X6["pass"], X6["win"]), 3), "flag": None})
    for lo, hi in ((1, 3), (4, 6), (7, 8), (9, 10)):
        v = [sum(X6["bid"][x][i] for x in range(lo, hi + 1)) for i in range(len(X6["win"]))]
        cards.append({"name": "Bid value %d-%d" % (lo, hi), "played_rate": round(sum(v) / (len(X6["win"]) * 14), 3), "win_correlation": round(pearson(v, X6["win"]), 3), "flag": None})
    for v in range(1, 5):
        cards.append({"name": "Lot printed value %d" % v, "played_rate": 1.0, "win_correlation": round(pearson(X6["lotval"][v], X6["win"]), 3),
                      "flag": "weak: printed value is swamped by Hype (Hype is %.0f%% of all points)" % (m6["hype_share_of_points"] * 100) if v == 1 else None})
    for c, nm in enumerate(("Clocks", "Silver", "Paintings", "Books")):
        cards.append({"name": "Category lots: " + nm, "played_rate": 1.0, "win_correlation": round(pearson(X6["lotcat"][c], X6["win"]), 3), "flag": None})
    mins = (m5["minutes"] + m6["minutes"]) / 2
    seat = {str(k): round(v, 3) for k, v in h["6p-allS"]["seat"].items()}
    P = [
     {"severity": "high", "problem": "Skill barely shows when several players play well: decisions do not separate good from random play at a mixed table.",
      "evidence": "3 strategic + 3 random (6p): strategic %.1f%% vs random %.1f%% per seat (5p: %.1f vs %.1f). A lone strategic bot among randoms wins %.1f%% (6p) / %.1f%% (5p), a gap of %.1f points, below the 20-point target. Best simple exploit found: pass 5 rounds then bid high, 26%% at 6p vs random, but banking en masse loses (3 bankers: 4-8%% each)." % (
        h["6p-SvR"]["bot"]["strategic"] * 100, h["6p-SvR"]["bot"]["random"] * 100, h["5p-SvR"]["bot"]["strategic"] * 100, h["5p-SvR"]["bot"]["random"] * 100,
        h["6p-oneS"]["bot"]["strategic"] * 100, h["5p-oneS"]["bot"]["strategic"] * 100, skill),
      "fix": "Give players information or leverage to act on (public hand sizes already exist; add a visible count of Paddles passed, or a second bid card choice), and make the bubble target readable earlier. Re-test E4 (bid 1-12) which lifted the lone-strategic share to 33% at 6p."},
     {"severity": "high", "problem": "Hype swamps printed lot values: lot value is a minor part of the score.",
      "evidence": "Hype is %.0f%% (5p) / %.0f%% (6p) of all points after the crash; printed values are ~40%%. Lot value 1 has the weakest link to winning (corr %.2f vs %.2f for value 3). E1 (lots +2) lowers Hype share to 46-53%% but raises unsold lots with strong bots (9.9 per game) and forced passes (34%%)." % (
        m5["hype_share_of_points"] * 100, m6["hype_share_of_points"] * 100, pearson(X6["lotval"][1], X6["win"]), pearson(X6["lotval"][3], X6["win"])),
      "fix": "Raise printed lot values moderately (e.g. 2-5, not +2 across the board) together with income 2, or accept Hype-driven scoring and say so in the pitch. Retest as a pair."},
     {"severity": "high", "problem": "Tied bids and empty hands leave many lots unsold; some rounds are dead.",
      "evidence": "Unsold lots per game: %.1f (5p mixed), %.1f (6p mixed), %.1f (6p all-strategic) of 28; %.1f bids per game are cancelled by ties (6p mixed). In the narrated game rounds 11 and 13 had zero bids and two lots worth up to 4 were wasted. Forced-pass (empty hand) rate is %.0f%% of player-rounds; mean hand is %.1f cards." % (
        m5["unsold_per_game"], m6["unsold_per_game"], h["6p-allS"]["unsold_per_game"], m6["cancelled_bids_per_game"], m6["forced_pass_rate"] * 100, m6["mean_hand"]),
      "fix": "Income 2 per pass (E2): unsold 7.8 -> 6.4 and forced passes 22% -> 13% in the all-strategic table, last-round winner flips 29% -> 19%. Also consider unsold lots carrying to the next round."},
     {"severity": "medium", "problem": "Last round decides a lot: the final burn decides which category crashes and flips the winner.",
      "evidence": "The leader before round 14 loses in %.0f%% (5p) / %.0f%% (6p) of games; the crash category changes in round 14 in %.0f%% / %.0f%% of games. Kingmaking is possible (a player out of contention can burn into a category), but this sim did not model deliberate kingmaking bots." % (
        m5["last_round_winner_flip"] * 100, m6["last_round_winner_flip"] * 100, m5["last_round_crash_flip"] * 100, m6["last_round_crash_flip"] * 100),
      "fix": "Hide nothing new: keep the swing but reduce it with income 2 (E2 flips 19%) or hand 5 (E5 flips 11% at 6p all-strategic, but runaway late 0.65)."},
     {"severity": "medium", "problem": "Ties in the final score are fairly common.", "evidence": "Shared/tied top score in %.1f%% (5p mixed) to %.1f%% (all-greedy 5p) of games, resolved by leftover cards." % (m5["ties"] * 100, h["5p-allG"]["ties"] * 100),
      "fix": "Acceptable; tiebreaker is clear. E2 cuts ties to 0.2-1.2%."},
     {"severity": "low", "problem": "Estimated length is at the low edge of the target.", "evidence": "Estimated %.1f min (14 rounds, my timing model: 25 s bid, 15 s reveal, 4 s per burned card, 6 s per lot, +3 min setup/scoring) vs 20 min target. With the designer's 70 s per round it would be 19.3 min. Real timing is untested." % mins,
      "fix": "Time with humans; if short, nothing to change."},
    ]
    j = {"verdict": "NEEDS-FIXES", "revision": 0, "games_simulated": 12 * N + 5 * 2 * (N // 2),
         "seat_win_rates": seat, "seat_balance_gap": round(spread(h["6p-allS"]), 1),
         "bot_win_rates": bw, "skill_expression": skill,
         "length": {"mean_turns": 14.0, "stdev": 0.0, "estimated_minutes": round(mins), "target_minutes": TARGET_MIN},
         "length_histogram": [{"turns": 14, "games": 12 * N}],
         "ties": round((m5["ties"] + m6["ties"]) / 2, 3), "turn_cap_hits": 0,
         "lead_changes_mean": round((m5["lead_changes"] + m6["lead_changes"]) / 2, 2),
         "runaway_leader_rate": round((m5["runaway_half"] + m6["runaway_half"]) / 2, 3),
         "cards": cards,
         "ambiguities": [
           "Which lot does a second bidder get if the first bidder takes one: the other (assumed, stated in rules).",
           "Round with zero Paddle-passers and an empty deck+discard: assumed no draw and no error (never reached in practice).",
           "Does 'nobody draws' apply to the income step of all passers or only when short: assumed all passers (happened in %.2f%% of 6p all-strategic games)." % (h["6p-allS"]["nodraw_per_game"] * 100),
           "Reshuffle timing: assumed the discard is shuffled only when a player must draw from an empty deck (mid-draw, so some passers may draw before and some after).",
           "Tiebreak 'bid value in hand' ties after cards-in-hand tie: shared win (assumed).",
           "Hype tie for top category: all tied categories crash (as written); this happens in a visible share of games and is very swingy.",
           "Bots treat hand sizes as public; Paddle vs Bid cards are indistinguishable face down, which does not matter in simulation."],
         "problems": P}
    json.dump(j, open(os.path.join(ROOT, "games", SLUG, "playtest.json"), "w"), indent=2)
    return j

if __name__ == "__main__":
    main()
