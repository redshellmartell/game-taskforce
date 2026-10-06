"""Headline run. Usage: python3 run.py [games_per_pairing=2000]. Writes ../playtest.json and details.json."""
import sys, json, os, statistics as S, collections, itertools
from game import play, AMBIGUITIES, NOTES, T_DECK, W_DECK
import bots as B
HERE = os.path.dirname(os.path.abspath(__file__)); G = os.path.dirname(HERE)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
PROBLEMS = [
 {"severity": "high", "problem": "The lead choice is solved again, now the other way: always lead yourself", "evidence": "Fixed policy vs the evaluating bot (2,000 games, both sides): always-lead-self wins 63%, always-give-lead wins 43% (KPI: each 40-60%). Fixed-policy mirrors (Treasurer win): self(T) vs give(W) 80%, give(T) vs self(W) 35%. The extra card is the cause: with no extra card (experiment E2) the policies fall to 47% and 50% but the lead choice then barely matters. Lead round-win rate is 54% (random bots 56%, greedy 44%).", "fix": "The extra card is too strong, no card is too weak. Untested ideas: the lead draws 1 card only when its hand is smaller (tested as E5: no better, self still 63%); try 'lead plays its first card face down' or 'lead reveals one hand card' as the price of last word instead of a card. Tested and rejected: no tie-win (E1, self 65%), ties to the second player (E4, self 59%), second player draws (E3, give 60% and Treasurer 85%)."},
 {"severity": "high", "problem": "Side gap too large and it flips with skill and lead habits", "evidence": "Equal-skill Treasurer win rate: random 57.8%, greedy 38.1%, strategic 37.9% (strategic mirror 36.6%, mixed pairings 27-41%). Headline seat gap 10.9 points (KPI 5). With fixed lead policies the strategic Treasurer wins 59% (both lead self) and 47% (both give). With no lead extra card (E2) the Treasurer wins 62%.", "fix": "Retune after the lead rule is settled: the Whisperer is favoured by skilled play (Hush, Retort), the Treasurer by random play. Lever 2 or 3 (Spend bonus, Treasury cap) in the designer's list, one at a time."},
 {"severity": "medium", "problem": "Games are short and often end in 2-3 rounds", "evidence": "Over 6,000 equal-skill games 31% end by round 3 (15% in round 2), only 29% reach round 7; strategic mirror is 97% throne endings, mean 3.9 rounds. A margin of 5 or more at position 1 wins the game on the spot. Estimated 12.7 minutes against a 15 target (-15%, inside the 20% limit).", "fix": "Raise the double-move margin to 6 or let the first throne approach be 4 steps (designer lever 9). The track is the main reason for lead changes landing at 1.8 not 2+."},
 {"severity": "medium", "problem": "Lead changes just below the KPI", "evidence": "1.83 per game over all pairings (strategic mirror 1.70), target 2.0.", "fix": "A longer track (shorter games fix and this together) or a bigger Murmurs draw; test double_at 6 first."},
 {"severity": "medium", "problem": "Strategic bot barely beats greedy, so deep decisions may be thin", "evidence": "Strategic wins 57.0% of games overall against greedy 59.2% (greedy leads itself and wins 57% as Treasurer vs strategic); strategic beats greedy only 42.8% (below 50%). Strategic beats random by 56 points, so decisions matter, but a simple greedy bot out-scores the heuristic, mostly through the lead choice.", "fix": "Fix the lead rule, then re-test with a smarter lead heuristic; may be bot weakness, not a design flaw."},
 {"severity": "low", "problem": "The Whisper (5 Influence plus Hush) is the one outlier card", "evidence": "Played in 79% of games, rounds with it won 17.6 points more than the Whisperer's average (flag: strong). No dead cards and no rarely played cards.", "fix": "Leave it, or drop to 4 Influence if the Whisperer side gap needs trimming."},
 {"severity": "low", "problem": "Rule ambiguities: none blocking, two minor interpretations", "evidence": "All 8 old ambiguities are resolved in v2. Two notes: Retort is only ever possible after a Treasurer card (clear); the lead's extra card is drawn after the Phase 1 draws (clear from the phase order, but easy to forget at the table).", "fix": "Optional: add a one-line reminder to the round summary."}]
MIN_PER_ACTION = 0.3; SETUP = 1.0

def lead_changes(h):
    sg = [x for x in ((d > 0) - (d < 0) for d in h) if x]
    return sum(1 for a, b in zip(sg, sg[1:]) if a != b)

def run_pair(a, b, n, base=0, collect=None):
    """a plays Treasurer (seat 1), b plays Whisperer (seat 2)."""
    res = dict(r3=0, r2=0, tw=0, ties=0, turns=[], rounds=[], lc=[], el=0, eln=0, end=collections.Counter(), pos0=0, nomove=0,
               leadw=0, leadn=0, resh=[0, 0], hush_blank=0, hush=0, retort=0, spend=0, hushed_spend=0, bank_lost=0, echo=0, dbl=0, tie_rounds=0, acts=[])
    for i in range(n):
        seed = base + i
        r = play((B.ALL[a](seed), B.ALL[b](seed + 7919)), seed); st = r["st"]; s = st.stats
        res["tw"] += r["winner"] == 0; res["turns"].append(r["turns"]); res["rounds"].append(r["rounds"]); res["acts"].append(s["actions"])
        res["lc"].append(lead_changes(st.history)); res["end"][r["end"]] += 1
        h = st.history; k = min(2, len(h) - 1)    # leader after round 2
        if len(h) > 2 and h[1]:
            res["eln"] += 1; res["el"] += ((h[1] < 0) == (r["winner"] == 0))
        res["r3"] += r["rounds"] <= 3; res["r2"] += r["rounds"] <= 2; res["nomove"] += s["tiebreak_noround"]; res["leadw"] += s["lead_won"]; res["leadn"] += s["lead_rounds"]
        res["resh"][0] += s["reshuf"][0]; res["resh"][1] += s["reshuf"][1]
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

def ablations():
    out = {}
    base_mirror = run_pair("plus", "plus", N, base=300000)["tw"] / N
    out["plus_mirror_T"] = base_mirror
    for nm, side in (("abl-nospend", 0), ("abl-nosteady", 0), ("abl-nohush", 1), ("abl-noretort", 1), ("abl-noecho", 1)):
        a, b = ("plus", nm) if side == 1 else (nm, "plus")
        t = run_pair(a, b, N, base=310000 + 1000 * len(out))["tw"] / N
        w = (t if side == 0 else 1 - t)       # ablation bot's win rate on its side
        base = base_mirror if side == 0 else 1 - base_mirror
        out[nm] = dict(side="T" if side == 0 else "W", abl_win=round(w, 3), full_win=round(base, 3), drop_pts=round((base - w) * 100, 1))
    return out

def variants():
    import game
    out = {}
    for label, kn in (("cap3", {"cap": 3}), ("court_off", {"court": 0}), ("cap2_base", {})):
        old = dict(game.KNOB); game.KNOB.update(kn)
        row = {}
        for a, b in (("strategic", "strategic"), ("plus", "plus"), ("greedy", "greedy"), ("random", "random")):
            r = run_pair(a, b, N, base=400000)
            row[a + " mirror"] = dict(T=round(r["tw"] / N, 3), lc=round(S.mean(r["lc"]), 2), r3=round(r["r3"] / N, 3), rounds=round(S.mean(r["rounds"]), 2))
        out[label] = row
        game.KNOB.clear(); game.KNOB.update(old)
    return out

def main():
    names = ["random", "greedy", "strategic"]
    cards = {0: {}, 1: {}, "games": 0}
    R3 = [0, 0]; pair = {}; allturns = []; allacts = []; alllc = []; el = eln = 0; ends = collections.Counter(); nomove = 0; tw = 0; tot = 0
    leadw = leadn = 0; resh = [0, 0]
    botwins = collections.Counter(); botgames = collections.Counter(); extra = collections.Counter()
    for a, b in itertools.product(names, names):
        r = run_pair(a, b, N, base=1000 * (names.index(a) * 3 + names.index(b)), collect=cards)
        pair[(a, b)] = r["tw"] / N
        tw += r["tw"]; tot += N; allturns += r["turns"]; allacts += r["acts"]; alllc += r["lc"]; el += r["el"]; R3[0] += r["r3"]; R3[1] += r["r2"]; eln += r["eln"]; ends += r["end"]; nomove += r["nomove"]
        leadw += r["leadw"]; leadn += r["leadn"]; resh[0] += r["resh"][0]; resh[1] += r["resh"][1]
        botwins[a] += r["tw"]; botwins[b] += N - r["tw"]; botgames[a] += N; botgames[b] += N
        for k in ("hush_blank", "hush", "retort", "spend", "hushed_spend", "bank_lost", "echo", "dbl", "tie_rounds"): extra[k] += r[k]
    # mirror strategic stats
    mirror = run_pair("strategic", "strategic", N, base=90000)
    seat_t = mirror["tw"] / N
    r3_all = sum(0 for _ in [])
    mir = dict(r3=mirror["r3"] / N, r2=mirror["r2"] / N, rounds=S.mean(mirror["rounds"]), T_win=seat_t, lead_changes=S.mean(mirror["lc"]), ends=dict(mirror["end"]), early=mirror["el"] / max(1, mirror["eln"]), turns=S.mean(mirror["turns"]),
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
    lp = {}
    det = dict(lead_policy_win_vs_strategic=lp, lead_round_win=leadw / leadn, reshuffles_per_game_T_W=[resh[0] / tot, resh[1] / tot], mirror=mir, pair_T_win={"%s(T) vs %s(W)" % k: round(v, 3) for k, v in pair.items()}, mirror_strategic_T_win=seat_t,
               strategic_vs_greedy=(sg_t + sg_w) / 2, greedy_vs_random=(gr_t + gr_w) / 2, ends=dict(ends), nomove_tiebreak=nomove,
               extra=dict(extra), mean_actions=mact, mean_rounds=None, tie_round_rate=extra["tie_rounds"] / sum(allturns) if False else None)
    det["ablations"] = ablations(); det["variants"] = variants()
    det["r3_by_pairing_all"] = None
    json.dump(det, open(os.path.join(HERE, "details.json"), "w"), indent=1)
    games = tot + N
    out = {"verdict": "NEEDS-FIXES", "revision": 2, "games_simulated": games,
           "seat_win_rates": {"1": round(S.mean(eq), 3), "2": round(1 - S.mean(eq), 3)}, "seat_balance_gap": round(seat_gap / 1, 1),
           "bot_win_rates": {n: round(botwins[n] / botgames[n], 3) for n in names}, "skill_expression": round(skill, 1),
           "length": {"mean_turns": round(mt, 1), "stdev": round(sd, 1), "estimated_minutes": mins, "target_minutes": 15},
           "length_histogram": [{"turns": t, "games": c} for t, c in sorted(hist.items())],
           "ties": round(extra["tie_rounds"] / tot, 3), "turn_cap_hits": 0,
           "lead_changes_mean": round(lc_mean, 2), "runaway_leader_rate": round(el / eln, 3) if eln else None,
           "cards": cardrows, "ambiguities": AMBIGUITIES,"ambiguity_notes": NOTES, "lead_round_win_rate": round(leadw / leadn, 3), "lead_policy_win_rates": lp, "reshuffles_per_game": {"treasurer": round(resh[0] / tot, 2), "whisperer": round(resh[1] / tot, 2)}, "problems": PROBLEMS}
    json.dump(out, open(os.path.join(G, "playtest.json"), "w"), indent=1)
    print("R3 all-pairings: by round3 %.3f by round2 %.3f" % (R3[0] / tot, R3[1] / tot)); det["by_round3_all"] = R3[0] / tot; det["by_round2_all"] = R3[1] / tot
    json.dump(det, open(os.path.join(HERE, "details.json"), "w"), indent=1)
    print("ABL", json.dumps(det["ablations"])); print("VAR", json.dumps(det["variants"]))
    print("games", games, "| equal-skill T win:", {n: round(pair[(n, n)], 3) for n in names}, "mirror strat T %.3f" % seat_t)
    print("T win by pairing (T row vs W col):")
    for a in names: print("  %-9s" % a, " ".join("%.3f" % pair[(a, b)] for b in names))
    print("MIRROR strategic:", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in mir.items()})
    print("bot win rates", out["bot_win_rates"], "skill gap strat-vs-random %.1f" % skill,
          "strat-vs-greedy %.3f greedy-vs-random %.3f" % ((sg_t + sg_w) / 2, (gr_t + gr_w) / 2))
    print("lead round-win %.3f | fixed lead policy game win vs evaluating bot: %s | reshuffles/game T %.2f W %.2f" % (leadw / leadn, {k: round(v, 3) for k, v in lp.items()}, resh[0] / tot, resh[1] / tot))
    print("seat gap %.1f | turns %.1f sd %.1f actions %.1f -> %.1f min" % (seat_gap, mt, sd, mact, mins))
    print("lead changes %.2f | early(R3)-leader wins %.3f | endings %s | pos0 tiebreak no-move %d" % (lc_mean, el / eln, dict(ends), nomove))
    print("per-game: hush %.2f blank %.2f retort %.2f spend %.2f hushed-spend %.2f bank-lost %.2f echo-ret %.2f double %.2f tie-rds %.2f" %
          tuple(extra[k] / tot for k in ("hush", "hush_blank", "retort", "spend", "hushed_spend", "bank_lost", "echo", "dbl", "tie_rounds")))
    fl = [(c["name"], c["played_rate"], c["win_correlation"], c["flag"]) for c in cardrows if c["flag"]]
    print("flagged cards:", fl)
main()
