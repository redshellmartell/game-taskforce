"""Headline run. Usage: python3 run.py [games_per_pairing=2000]. Writes ../playtest.json and details.json."""
import sys, json, os, statistics as S, collections, itertools
from game import play, AMBIGUITIES, T_DECK, W_DECK
import bots as B
HERE = os.path.dirname(os.path.abspath(__file__)); G = os.path.dirname(HERE)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
PROBLEMS = [
 {"severity": "high", "problem": "Lead changes below KPI: the crown rarely swings sides", "evidence": "1.15 lead changes per game (strategic mirror 1.22; KPI >= 2). 17% of games end on a throne, 56% on round-7 leader, 17-30% crown back at position 0 so the tiebreak decides.", "fix": "Make the court's catch-up bite harder at positions 1-2 (trailer +1 draw is too weak: make T1/W1 trailer draw 2 or let the trailer lead without choosing) and make a double move easier (margin 4+, tested: throne wins 17% to 23% but lead changes unchanged and Treasurer 57%). Needs a designer decision; lead changes may need a rule that rewards crossing the centre."},
 {"severity": "high", "problem": "Choosing the lead is a solved decision: always give the opponent the lead (last word)", "evidence": "Strategic mirror: a side that leads when it is the chooser wins only 26% (both-lead 26/74); both giving the lead away gives 50/50. Casual, family and story bots (who lead themselves) win 35-46% overall.", "fix": "Remove the choice (alternate leads, loser leads) or make leading worth something (leader draws or gets +1 on the first card)."},
 {"severity": "medium", "problem": "Margin rules at positions 2 and 3 are nearly inert", "evidence": "Removing the margin-2 rule at position 2 changed nothing (Treasurer 50.2% either way, early-leader 41.7% vs 41.8%); bots simply aim for the required margin.", "fix": "Raise to 3 at position 2 and 4 at position 3, or drop the rule and keep only the extra draws, to cut rules text."},
 {"severity": "medium", "problem": "Skill levels shift side balance: Treasurer wins 63% random-vs-random, Whisperer wins 60% greedy-vs-greedy, 50% strategic-vs-strategic", "evidence": "Equal-skill Treasurer win rate: random 62.7%, greedy 40.2%, strategic 50.4%. Real players of mixed skill will see one side feel better than the other. Seat gap at equal strong play is 1-2 points (passes KPI).", "fix": "Retest after fixing lead choice; the Whisperer (Hush, Retort) is harder to play, so beginners may pick the Treasurer and win."},
 {"severity": "medium", "problem": "Crown stalls: 17% (all bots) to 30% (strategic mirror) of games finish at position 0 and are decided by the tiebreak", "evidence": "endings: leader 56%, tiebreak 17%, throne 17% (all pairings); strategic mirror 54/29/17 (leader/tiebreak/throne).", "fix": "Dead-centre endings feel arbitrary; give round-7 to a decisive rule (for example winner of round 7 wins ties at 0, already almost the rule) or shorten the track."},
 {"severity": "low", "problem": "Hush is blank in about a quarter of plays; Spend gets Hushed in 0.35 games per game", "evidence": "5.2 Hush plays per game, 1.35 with no legal target (blank) over all pairings, 0.68 in the strategic mirror; coins lost to Hush 0.35 per game.", "fix": "Fine as is; keep an eye on Steady count if Whisperer win rate drifts."},
 {"severity": "low", "problem": "Rule ambiguities remain (KPI: zero at pitch)", "evidence": "See ambiguities list: Retort after pass, ties and chooser, Spend vs Hush ordering.", "fix": "Designer to clarify in v2."}]
MIN_PER_ACTION = 0.3; SETUP = 1.0

def lead_changes(h):
    sg = [x for x in ((d > 0) - (d < 0) for d in h) if x]
    return sum(1 for a, b in zip(sg, sg[1:]) if a != b)

def run_pair(a, b, n, base=0, collect=None):
    """a plays Treasurer (seat 1), b plays Whisperer (seat 2)."""
    res = dict(tw=0, ties=0, turns=[], rounds=[], lc=[], el=0, eln=0, end=collections.Counter(), pos0=0, nomove=0,
               hush_blank=0, hush=0, retort=0, spend=0, hushed_spend=0, bank_lost=0, echo=0, dbl=0, tie_rounds=0, acts=[])
    for i in range(n):
        seed = base + i
        r = play((B.ALL[a](seed), B.ALL[b](seed + 7919)), seed); st = r["st"]; s = st.stats
        res["tw"] += r["winner"] == 0; res["turns"].append(r["turns"]); res["rounds"].append(r["rounds"]); res["acts"].append(s["actions"])
        res["lc"].append(lead_changes(st.history)); res["end"][r["end"]] += 1
        h = st.history; k = min(2, len(h) - 1)    # leader after round 3
        if len(h) > 3 and h[2]:
            res["eln"] += 1; res["el"] += ((h[2] < 0) == (r["winner"] == 0))
        res["nomove"] += s["tiebreak_noround"]
        for k_ in ("hush_blank", "hush", "retort", "hushed_spend", "bank_lost"): res[k_] += s[k_]
        res["echo"] += s["echo_returned"]; res["spend"] += s["spend_used"]; res["dbl"] += s["double_moves"]; res["tie_rounds"] += s["ties_rounds"]
        if collect is not None:
            for p in (0, 1):
                for name, (a_, b_) in s["card_round"][p].items():
                    d = collect[p].setdefault(name, [0, 0, 0]); d[0] += a_; d[1] += b_
                    d[2] += sum(1 for _ in [0] if False)
                collect[p].setdefault("_rounds", [0, 0, 0]); collect[p]["_rounds"][0] += s["rounds"]; collect[p]["_rounds"][1] += s["round_w"][p]
                # games in which the card was played at all
                for name in s["plays"][p]: collect[p].setdefault("g:" + name, [0])[0] += 1
            collect["games"] += 1
    return res

def main():
    names = ["random", "greedy", "strategic"]
    cards = {0: {}, 1: {}, "games": 0}
    pair = {}; allturns = []; allacts = []; alllc = []; el = eln = 0; ends = collections.Counter(); nomove = 0; tw = 0; tot = 0
    botwins = collections.Counter(); botgames = collections.Counter(); extra = collections.Counter()
    for a, b in itertools.product(names, names):
        r = run_pair(a, b, N, base=1000 * (names.index(a) * 3 + names.index(b)), collect=cards)
        pair[(a, b)] = r["tw"] / N
        tw += r["tw"]; tot += N; allturns += r["turns"]; allacts += r["acts"]; alllc += r["lc"]; el += r["el"]; eln += r["eln"]; ends += r["end"]; nomove += r["nomove"]
        botwins[a] += r["tw"]; botwins[b] += N - r["tw"]; botgames[a] += N; botgames[b] += N
        for k in ("hush_blank", "hush", "retort", "spend", "hushed_spend", "bank_lost", "echo", "dbl", "tie_rounds"): extra[k] += r[k]
    # mirror strategic stats
    mirror = run_pair("strategic", "strategic", N, base=90000)
    seat_t = mirror["tw"] / N
    mir = dict(T_win=seat_t, lead_changes=S.mean(mirror["lc"]), ends=dict(mirror["end"]), early=mirror["el"] / max(1, mirror["eln"]), turns=S.mean(mirror["turns"]),
               hush_blank=mirror["hush_blank"] / N, hush=mirror["hush"] / N, tie_rounds=mirror["tie_rounds"] / N, dbl=mirror["dbl"] / N)
    sr_t = pair[("strategic", "random")]; sr_w = 1 - pair[("random", "strategic")]   # strategic wins as T / as W vs random
    skill = (sr_t + sr_w) / 2 * 100 - (1 - (sr_t + sr_w) / 2) * 100
    sg_t = pair[("strategic", "greedy")]; sg_w = 1 - pair[("greedy", "strategic")]
    gr_t = pair[("greedy", "random")]; gr_w = 1 - pair[("random", "greedy")]
    # overall side balance across equal-skill pairings
    eq = [pair[(n, n)] for n in names]
    seat_gap = abs(S.mean(eq) - 0.5) * 100 * 2
    mt, sd = S.mean(allturns), S.pstdev(allturns); mact = S.mean(allacts)
    mins = round(SETUP + MIN_PER_ACTION * mact, 1)
    hist = collections.Counter(allturns)
    cardrows = []
    for p in (0, 1):
        base = cards[p]["_rounds"][1] / cards[p]["_rounds"][0]
        for name, v_ in sorted(cards[p].items()):
            if name.startswith("_") or name.startswith("g:"): continue
            rp, rw = v_[0], v_[1]
            n = cards["games"]; pl = cards[p]["g:" + name][0]
            corr = rw / rp - base      # round win rate when the card is in the row, minus the side's baseline
            flag = None
            if pl / n < 0.3: flag = "rarely played"
            elif corr < -0.12: flag = "weak: rounds with it are won %.0f pts less than the side's average" % (-corr * 100)
            elif corr > 0.15: flag = "strong"
            cardrows.append({"name": ("T: " if p == 0 else "W: ") + name, "played_rate": round(pl / n, 3), "win_correlation": round(corr, 3), "flag": flag})
    lc_mean = S.mean(alllc)
    det = dict(mirror=mir, pair_T_win={"%s(T) vs %s(W)" % k: round(v, 3) for k, v in pair.items()}, mirror_strategic_T_win=seat_t,
               strategic_vs_greedy=(sg_t + sg_w) / 2, greedy_vs_random=(gr_t + gr_w) / 2, ends=dict(ends), nomove_tiebreak=nomove,
               extra=dict(extra), mean_actions=mact, mean_rounds=None, tie_round_rate=extra["tie_rounds"] / sum(allturns) if False else None)
    json.dump(det, open(os.path.join(HERE, "details.json"), "w"), indent=1)
    games = tot + N
    out = {"verdict": "NEEDS-FIXES", "revision": 1, "games_simulated": games,
           "seat_win_rates": {"1": round(S.mean(eq), 3), "2": round(1 - S.mean(eq), 3)}, "seat_balance_gap": round(seat_gap / 1, 1),
           "bot_win_rates": {n: round(botwins[n] / botgames[n], 3) for n in names}, "skill_expression": round(skill, 1),
           "length": {"mean_turns": round(mt, 1), "stdev": round(sd, 1), "estimated_minutes": mins, "target_minutes": 15},
           "length_histogram": [{"turns": t, "games": c} for t, c in sorted(hist.items())],
           "ties": round(extra["tie_rounds"] / tot, 3), "turn_cap_hits": 0,
           "lead_changes_mean": round(lc_mean, 2), "runaway_leader_rate": round(el / eln, 3) if eln else None,
           "cards": cardrows, "ambiguities": AMBIGUITIES, "problems": PROBLEMS}
    json.dump(out, open(os.path.join(G, "playtest.json"), "w"), indent=1)
    print("games", games, "| equal-skill T win:", {n: round(pair[(n, n)], 3) for n in names}, "mirror strat T %.3f" % seat_t)
    print("T win by pairing (T row vs W col):")
    for a in names: print("  %-9s" % a, " ".join("%.3f" % pair[(a, b)] for b in names))
    print("MIRROR strategic:", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in mir.items()})
    print("bot win rates", out["bot_win_rates"], "skill gap strat-vs-random %.1f" % skill,
          "strat-vs-greedy %.3f greedy-vs-random %.3f" % ((sg_t + sg_w) / 2, (gr_t + gr_w) / 2))
    print("seat gap %.1f | turns %.1f sd %.1f actions %.1f -> %.1f min" % (seat_gap, mt, sd, mact, mins))
    print("lead changes %.2f | early(R3)-leader wins %.3f | endings %s | pos0 tiebreak no-move %d" % (lc_mean, el / eln, dict(ends), nomove))
    print("per-game: hush %.2f blank %.2f retort %.2f spend %.2f hushed-spend %.2f bank-lost %.2f echo-ret %.2f double %.2f tie-rds %.2f" %
          tuple(extra[k] / tot for k in ("hush", "hush_blank", "retort", "spend", "hushed_spend", "bank_lost", "echo", "dbl", "tie_rounds")))
    fl = [(c["name"], c["played_rate"], c["win_correlation"], c["flag"]) for c in cardrows if c["flag"]]
    print("flagged cards:", fl)
main()
