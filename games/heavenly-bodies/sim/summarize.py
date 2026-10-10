"""Builds ../playtest.json and prints a compact (<40 line) KPI summary from results_head/abl/exp.json (run run.py first)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
L = lambda p: json.load(open(os.path.join(HERE, p)))
d = L("results_head.json")["head"]; a = L("results_abl.json")["abl"]; e = L("results_exp.json")["exp"]; e5 = L("experiments/e5_burst.json")
m = d["mirror2"]; pr = d["pairs"]; ba = d["bot_avg"]
gap = abs(m["seat"][0] - m["seat"][1]) * 50
skill = (1 - pr["random_v_strategic"] - pr["random_v_strategic"]) * 100
minutes = m["turns"] * 1.0 + 3.0
star2 = {k: v["win"] for k, v in d["stars2"].items()}
stars_bad = {k: round(v * 100, 1) for k, v in star2.items() if not 0.40 <= v <= 0.60}
cards = []
for cid, v in d["cards2"].items():
    c = d["cards4"][cid]; flag = None
    if v["played"] < 0.05 and c["played"] < 0.10: flag = "rarely played (2p %.1f%%, 4p %.1f%% of games)" % (v["played"] * 100, c["played"] * 100)
    elif v["link"] > 0.2 and v["played"] > 0.05: flag = "winning link +%.2f (finisher effect; no-burst bot loses 4.6 points at 2p, 0 at 4p)" % v["link"]
    cards.append(dict(name=cid, played_rate=round(v["played"], 3), win_correlation=round(v["link"], 3), flag=flag))
games = 16000 + 6600 + 2000 + 40000 + 40000 + 4000 + 600
problems = [
 dict(severity="high", problem="Rotation direction is inert: the always-clockwise bot loses by under 1 point",
      evidence="Always-clockwise vs the direction-choosing bot: 49.1% at 2p (margin 0.9), 22.6% at 4p (margin 2.4); ignore-North bot 49.7% / 25.1% (margins 0.3 / -0.1). Target 5+. The decision exists (directions differ in value in 60% of Rotation Phases, by over 1 point in 33%; North term flips the choice in 26%) but a wrong choice costs little; rotation Collisions are 0.33 per game, total Collisions 0.73.",
      fix="Make direction costly or rewarding: e.g. a bigger North payoff/penalty (AE22-type cards at 2 or 3 damage-equivalent), more cards that score on a position (E/S/W bonuses), or retire the choice. Bot blindness possible; needs a human check."),
 dict(severity="high", problem="Star balance follows HP; HP 5 Stars are hopeless in free-for-all",
      evidence="2p round-robin (1,100 games per Star): outside 40-60: " + ", ".join("%s %s%%" % kv for kv in stars_bad.items()) + ". 4p random tables (about 650 games per Star): HP8 43/37/48%, HP7 31/40/33%, HP6 17/19/20%, HP5 8/3/4% (fair 25). ST11's ability is inert (on vs off 52.4% vs 50 at 2p, +0.6 at 4p). The strategic bot focus-fires the lowest HP (a bot rule), so part of the 4p gap is bot-dependent and unconfirmed.",
      fix="ST11: a stronger reclaim loop (reclaim any Size, or damage 2) or HP 6. HP 5 Stars at 4p+ need a defensive ability. ST05 (HP 7) is strongest at 2p, 65%; check a second targeting bot."),
 dict(severity="medium", problem="6-player Critical Mass share is under 40%; the 17 cap overshoots toward Star Destruction",
      evidence="Strategic mirror 2000 games: 2p 50.3% CM, 3p 48.4%, 4p 50.7%, 5p 41.9% (CI 39.8-44.1), 6p 38.0% (CI 35.8-40.1). Single change: 6p at threshold 16 gives 50.2% CM (36.3% at 17 in the same run), 5p at 16 gives 56.4% (43.7% at 17). Flat 15 gives 2p 39% / 4p 62% / 6p 64% CM, so the scaling is doing its job.",
      fix="Threshold 17 at 5p, 16 at 6p (or 12+players capped at 17 with 6p printed as 16). One number."),
 dict(severity="medium", problem="AE25 and AE28 still have a high winning link",
      evidence="Winning link AE25 +%.2f, AE28 +%.2f (target under 0.2; was +0.26 / +0.42). Causal check: a bot that never plays them loses 4.6 points at 2p and about 0 at 4p, so most of the link is selection (they are played when a kill is near). Played in %.0f%% and %.0f%% of 2p games." % (d["cards2"]["AE25"]["link"], d["cards2"]["AE28"]["link"], d["cards2"]["AE25"]["played"] * 100, d["cards2"]["AE28"]["played"] * 100),
      fix="Judge them by the causal 4.6 points, not the link; if a lower number is wanted, 2 damage on AE25 (cost 2 hurts little at 2p)."),
 dict(severity="medium", problem="Dead cards: 3.3 per 7-card hand on an empty board (target under 3)",
      evidence="%.2f dead cards per 7-card hand (was 3.43); %.1f%% of hands have no CO (mulligan fixes those). Real turn 1: %.1f%% of first turns make 2 plays. Rarely played cards: AE14 (1.5%%), AE04, AE08, AE17, AE49 under 5%% at 2p." % (d["dead"]["per_hand"], d["dead"]["no_co"] * 100, d["turn_plays"]["t1_two"] * 100),
      fix="Mostly structural (22 Augmentations need a host). Recycle exists but is not worth taking for the bots (see next). Consider 2 more COs for AEs, or a free draw-to-CO rule."),
 dict(severity="medium", problem="Recycle and the mulligan do not help the bots",
      evidence="Never-recycle bot beats the recycling bot: 54.9% at 2p (-4.9 margin), 25.1% at 4p. Never-mulligan bot 51.3% / 24.2% (margin -1.3 / 0.8). Recycle is used 1.5 times per 2p game.",
      fix="Either make Recycle free once per turn or accept that it is a clog valve (a human check on hand clog is needed; bots do not feel hand clog)."),
 dict(severity="low", problem="ST12's and ST11's single-change effects",
      evidence="ST12 free -1 Stability: ST12 wins 41.7% at 2p with it, 29.8% without (+11.9), and shifts 2p games toward Star Destruction (CM share 31.7% vs 40.9%); at 4p 4.2% vs 3.7%. It is not too strong; ST12 stays below fair. The ST11 reclaim loop is inert: 30.3% on vs 29.1% off at 2p, 4.4% vs 4.2% at 4p.",
      fix="Leave ST12; rework ST11 (see problem 2)."),
 dict(severity="low", problem="AE58 and CO18 are weak under the plain-rotation rule",
      evidence="Card rotations ignore anchors and cannot Collide (rules 5.2), so rotating an opponent's orbit only changes bonus positions; AE58 and CO18 are mostly a cantrip / free ping. Played in 15% and 19% of 2p games.",
      fix="Give them a payoff (rotate then North hit) or accept."),
]
out = dict(verdict="NEEDS-FIXES", revision=1, games_simulated=games,
  seat_win_rates={"1": round(m["seat"][0], 3), "2": round(m["seat"][1], 3)}, seat_balance_gap=round(gap, 1),
  bot_win_rates={k: round(v, 3) for k, v in ba.items()}, skill_expression=round(skill, 1), bot_spread=round(d["spread"] * 100, 1),
  length=dict(mean_turns=round(m["turns"], 1), stdev=round(m["turns_sd"], 1), estimated_minutes=round(minutes, 1), target_minutes=12,
              note="turns = player turns (2p); minutes = 1 per player turn + 3 setup (estimate). 3p/4p/5p/6p: %s turns" % ", ".join("%.0f" % d["split"][str(n)]["turns"] for n in (3, 4, 5, 6))),
  length_histogram=[dict(turns=int(t), games=g) for t, g in m["hist"].items()],
  ties=0.0, turn_cap_hits=0, lead_changes_mean=round(m["lc"], 2), runaway_leader_rate=round(m["runaway"], 3),
  win_path={str(n): dict(cm=round(d["split"][str(n)]["cm"], 3), star=round(1 - d["split"][str(n)]["cm"], 3), cm_ci=d["split"][str(n)]["cm_ci"]) for n in (2, 3, 4, 5, 6)},
  star_win_rates_2p={k: round(v, 3) for k, v in star2.items()}, star_win_rates_4p={k: round(v["win"], 3) for k, v in d["stars4"].items()},
  cm_cancel_share_2p=round(m["cmev"]["cancel_share"], 3),
  ablations={k: {n: dict(rate=round(v["rate"], 3), margin=round(v["margin"], 1)) for n, v in a[k].items()} for k in ("always_cw", "ignore_north", "no_recycle", "no_mull")},
  ability_off={s: {n: dict(on=round(v["on"], 3), margin=round(v["margin"], 1)) for n, v in o.items()} for s, o in a["ability"].items()},
  flat15={n: round(v["cm"], 3) for n, v in a["flat15"].items()},
  experiments=e, burst_ablation=e5, cards=cards,
  ambiguities=["AE60: a CO that moves into North moves even if anchored (AE16/AE14/CO27); the Collision uses effective values in North (coded yes)",
    "AE49 with fewer than 4 cards in the deck: look at what is there and reshuffle only when empty (5.6 does not say how many to look at)",
    "ST11 / AE45 'Size 3 or less' for a CO in the Out of Orbit zone: printed Size (zone has no modifiers)",
    "ST11 damage when the reclaimed CO loses its Collision: still deals damage (reclaim happened)",
    "Critical Mass cancel check per card/ability/trigger (5.5 wording) vs per play: coded per play, per Rotation Phase and per End of Turn; enters-trigger inside a play is not a separate check",
    "AE28 'Size 4 or more': effective Size when the cost is paid (coded)",
    "Recycle with draw deck and discard both empty: coded as not offered (discard-then-draw would return the same card)",
    "LIFO stack: the active player's choice of order among their own simultaneous triggers (AE09, AE11, CO23, AE20) is arbitrary in the sim; results do not depend on it"],
  problems=problems)
json.dump(out, open(os.path.join(HERE, "..", "playtest.json"), "w"), indent=1)
print("verdict NEEDS-FIXES | games %d" % games)
print("seat gap 2p %.1f | strat v random gap %.1f | strat v greedy %.1f%% | spread %.1f" % (gap, skill, (1 - pr["greedy_v_strategic"]) * 100, d["spread"] * 100))
print("length 2p %.1f turns %.1f min | 3-6p turns %s" % (m["turns"], minutes, "/".join("%.0f" % d["split"][str(n)]["turns"] for n in (3, 4, 5, 6))))
print("CM share 2..6p: " + " ".join("%.0f" % (d["split"][str(n)]["cm"] * 100) for n in (2, 3, 4, 5, 6)) + " | cancel share 2p %.0f%%" % (m["cmev"]["cancel_share"] * 100))
print("runaway 2p %.1f%% | lead changes %.2f | dead/hand %.2f" % (m["runaway"] * 100, m["lc"], d["dead"]["per_hand"]))
print("stars outside 40-60 (2p):", stars_bad)
print("ablation margins 2p/4p: cw %.1f/%.1f north %.1f/%.1f norecycle %.1f/%.1f nomull %.1f/%.1f" % tuple(x for k in ("always_cw", "ignore_north", "no_recycle", "no_mull") for x in (a[k]["2"]["margin"], a[k]["4"]["margin"])))
print("ability margins 2p/4p:", {s: (round(o["2"]["margin"], 1), round(o["4"]["margin"], 1)) for s, o in a["ability"].items()})
