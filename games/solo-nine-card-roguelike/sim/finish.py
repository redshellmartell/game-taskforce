"""Builds ../playtest.json (rules v2, revision 1) from results.json + experiments/ablate-*.json + a 30k-layout card/win sample."""
import itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from game import play, NAMES, TRICKS
import bots as B
R = json.load(open(os.path.join(HERE, "results.json"))); P = json.load(open(os.path.join(HERE, "..", "playtest.json")))
S, L, Rd, G = R["strategic"], R["lookahead"], R["random"], R["greedy"]
AO = json.load(open(os.path.join(HERE, "experiments", "ablate-strategic-4-none.json")))
AD = json.load(open(os.path.join(HERE, "experiments", "ablate-strategic-4-123.json")))
AL = json.load(open(os.path.join(HERE, "experiments", "ablate-lookahead-400-none.json")))
prev = P["solo_targets"] if "previous" not in P else P["previous"]["solo_targets"]
cnt = {c: [0, 0, 0, 0] for c in range(1, 10)}; ucnt = {c: [0, 0, 0, 0] for c in TRICKS}
for pm in itertools.islice(itertools.permutations(range(1, 10)), 0, 362880, 12):
    r = play(pm, (), B.Strategic()); b = set(r.stats["beaten"]); u = set(r.stats["tricks"])
    for c in range(1, 10):
        cnt[c][0 if c in b else 2] += 1; cnt[c][1 if c in b else 3] += r.won
    for c in TRICKS:
        if c in r.stats["ever_ready"]: ucnt[c][0 if c in u else 2] += 1; ucnt[c][1 if c in u else 3] += r.won
f = lambda a, b: a / b if b else None
fl = {"Crow": "dead trick: Carry used in 0.7% of outline and 0.07% of lookahead runs where Ready; ablation 0.0 points; swap never fires",
      "Spider": "Silk used 16.7% (outline) / 7.5% (lookahead); removing Silk RAISES outline win by 3.8 points",
      "Moth": "Glow used 72% / 56% but ablation only +2.8 (outline) and 0.0 (lookahead)",
      "Fox": "Feint used 13.0% (outline, <15%), 100% (lookahead); outline ablation +0.9",
      "Snake": "Hypnotise ablation +3.6 (outline), below the +5 bar",
      "Owl": "spend-Owl-first ablation +0.9 (inert choice); Wise changes wounds in 92% of Owl runs"}
cards = []
for c in range(1, 10):
    nm = NAMES[c]; d = dict(name=nm, played_rate=round(S["beaten"].get(nm, 0), 3), shoved_rate=round(S["shoved"].get(nm, 0), 3))
    if c in TRICKS:
        d["trick_use_given_ready_outline"] = S["trick_use_given_ready"].get(nm); d["trick_use_given_ready_lookahead"] = L["trick_use_given_ready"].get(nm)
        x = f(ucnt[c][1], ucnt[c][0]); y = f(ucnt[c][3], ucnt[c][2]); d["win_correlation"] = round(x - y, 3) if x is not None and y is not None else None
    else:
        d["win_correlation"] = round(f(cnt[c][1], cnt[c][0]) - f(cnt[c][3], cnt[c][2]), 3) if cnt[c][0] and cnt[c][2] else None
    d["flag"] = fl.get(nm); cards.append(d)
gh = {k: round((v - S["win_rate"]) * 100, 1) for k, v in R["ghost"].items()}
ab = lambda A, k: round((A["full"]["win"] - A[k]["win"]) * 100, 1)
ablation = dict(outline_points_full_minus_ablated={k: ab(AO, k) for k in AO if k != "full"}, outline_drift_with_ghosts_1_2_3=ab(AD, "drift") if "drift" in AD else None,
                outline_anger_off_points=-19.8, lookahead_points_full_minus_ablated={k: ab(AL, k) for k in AL if k != "full"},
                note="needs >= +5; Glow, Silk, Carry, Carry-no-swap, Hypnotise, Feint, Owl-first fail; Dart, Scavenge, Shove, Drift pass; Anger off wins +19.8 so Anger is a real cost")
amb = ["Rule 5 Silk: 'Silk needs a Lit calm card and a Dark card' - implemented; whether Silk may Shove the same card twice in a turn (Silk then normal Shove of the same card X, now Dark/calm) is unstated; implemented as legal because Silk leaves it calm",
       "Carry swap of two Dark cards: legal ('any two grid cards') but the player learns nothing; implemented as legal, bots only swap a known Hound",
       "A Ghost Moth/Mouse/Spider that is Dark and is later turned face up by Lighting at Phase 3 / after a Fight: Drift is Phase 1 only, so it waits a turn (implemented as written); the Hound Hunt resolves first in the meantime",
       "Drift takes the card 'Ready' but the rules do not say whether Drift can happen when the Ghost is Angry (implemented: yes, Angry resets on leaving the grid)",
       "Scavenge readying a trophy whose trick was already used this turn: implemented as once per turn (rules v2 says so; closed)",
       "Hunt when the Hound is lit by the Phase 1 Drift or a Silk Shove (closed in v2, implemented as written)",
       "Old gaps still open: strategic outline step 'Hide' wording does not say that a normal Shove makes the Hound Angry (Danger 11), which in the sim makes a hidden Hound nearly unbeatable without Feint or Hypnotise"]
problems = [
 dict(severity="high", problem="Strong play is nearly free: lookahead bot wins 96.1% (sanity cap 90%); only the outline bot sits in a believable band (57.1%), at the top of the 25-60 band",
      evidence="Exhaustive 362,880 layouts outline 57.1% (was 19.1%); lookahead 3,632 layouts 96.1% (was 80.8%); greedy 11.2%; random 0.0%. Lookahead sessions: 96% score 9. v2 removed Thief, softened Ghosts, freed Glow and Silk: everything made the game easier",
      fix="Use the designer's knob: Hunt lethal (no Ready trophy at Hunt = dead). Tested: lookahead 96.1 to 77.0 (907 layouts), outline 57.1 to 56.4 (every 8th layout), spread 39 to 21 points. Re-run both bots after adopting it"),
 dict(severity="high", problem="Carry is still a dead card; Silk and Glow barely matter; Feint, Hypnotise and Owl-first fail the ablation bar",
      evidence="Where Ready, Carry used 0.7% (outline) and 0.07% (lookahead); ablation 0.0 points both bots; Carry no-swap ablation identical (swap fired in 0.5% of outline runs, 0% lookahead). Silk: removing it gains the outline +3.8 points, lookahead +0.55. Glow +2.8 / 0.0. Hypnotise +3.6, Feint +0.9, Owl-first +0.9 (outline). Passing: Dart +12.0, Scavenge +24.5, Shove +28, Drift +13 (Ghosts 1,2,3), Anger off -19.8 (Anger is a real cost)",
      fix="Cut Carry's swap or the whole Crow trick (it is -2 Danger for one trophy, always worse than Dart or just fighting); make Silk give something (for example no spend of the Spider) or cut it; accept Glow as flavour or tie it to the Hound. Test with a bot that models the changed card"),
 dict(severity="medium", problem="Single-Ghost lift is uneven: tiny for small Ghosts, negative for Rat, too big for the Hound",
      evidence="Outline, per Ghost: Moth +4.1, Mouse +4.4, Spider +1.9, Rat -3.7, Crow +14.8, Owl +20.7, Snake +13.9, Fox +13.0, Hound +39.0 (target +5 to +25; v1 was +0.0, +0.1, +1.4, +21, +38, +44, +29, +43, +19). Four of nine in band. The lookahead bot cannot show lifts (ceiling 96%). Rat negative is unexplained (untested guess: a Danger 2 Rat is fought early and wastes the Scavenge reserve)",
      fix="Ghost Hound Danger 7 with no Hunt is worth 39 points: keep Danger 8 or keep Hunt for a Ghost Hound; let Drift apply to the Rat so that it matches the small Ghosts"),
 dict(severity="medium", problem="Variety targets missed: killer spread, Feint share and session shape",
      evidence="Outline killers: Hound 64.9%, Fox 30.9%, all others under 3.4% (only 2 cards over 5%; target 4). Lookahead: Hound 9.9% (target 40-75%), 8 cards over 5%. Feint share of wins 2.4% / 9.9% (target >=10%); Hypnotise 9.9% / 19.6%. Sessions: outline 54% end on score 8 (target <=40%), lookahead 96% on score 9; mean 2.8 / 2.0 runs (target 3-4)",
      fix="Hunt lethal should raise Hound deaths for the strong player; re-measure. Fox is the real gate for the outline bot (31% of deaths)"),
 dict(severity="medium", problem="Grinding opening and the Angry Hound trap",
      evidence="Outline: first action is a Fight on 63% of layouts; first Fight arrives on turn 3 or later in 24% and turn 4 or later in 13% (narrated seed 2: five Shoves in a row, then dead to an Angry Hound, Danger 11). Lookahead opens with a Shove 89.6% (target 20-60%). Hiding the Hound by a normal Shove makes it Danger 11",
      fix="Say in the rules that Shoving the Hound angers it (+2); consider letting Silk be the only safe hide. Human sessions needed to judge the opening"),
 dict(severity="low", problem="Length is inside the band but the strong bot is slower than the outline",
      evidence="Outline mean 8.33 turns (median 8, 8.3 min); lookahead mean 9.22 (median 10, 9.2 min); target 10 min (-17% / -8%). Turn cap 20: 0 hits in ~1.1M runs. Previous: outline 6.68 turns (6.4 min), lookahead 8.44 (8.3 min)",
      fix="None")]
mean = L["mean_turns"]
out = dict(verdict="NEEDS-FIXES", verdict_note="bots only, unvalidated", revision=1, games_simulated=362880 * 3 + 3632 + 907 * 4 + 90720 * 13 + 20000 + 150 + 3 * 45360 + 100000,
  seat_win_rates={"1": 1.0}, seat_balance_gap=0.0,
  bot_win_rates={"random": Rd["win_rate"], "greedy": G["win_rate"], "strategic": S["win_rate"], "lookahead": L["win_rate"]},
  skill_expression=round((L["win_rate"] - Rd["win_rate"]) * 100, 1), skill_expression_outline=round((S["win_rate"] - Rd["win_rate"]) * 100, 1),
  bot_spread_points=round((L["win_rate"] - S["win_rate"]) * 100, 1),
  length=dict(mean_turns=round(mean, 2), stdev=round(L["stdev_turns"], 2), estimated_minutes=round(L["est_minutes"], 1), target_minutes=10,
              outline_mean_turns=round(S["mean_turns"], 2), outline_minutes=round(S["est_minutes"], 1), outline_median=S["median_turns"], lookahead_median=L["median_turns"]),
  length_histogram=[dict(turns=t, games=c) for t, c in S["length_hist"]], length_histogram_bot="outline, 362,880 layouts",
  ties=0.0, turn_cap_hits=0, lead_changes_mean=None, runaway_leader_rate=None,
  solo_notes="Seat balance, lead changes and runaway leader do not apply to a solo game.",
  solo_targets=dict(win_rate_band=[0.40, 0.60], outline_win_rate=S["win_rate"], lookahead_win_rate=L["win_rate"],
    wins_feint=dict(outline=S["wins_feint"], lookahead=L["wins_feint"]), wins_hypno=dict(outline=S["wins_hypno"], lookahead=L["wins_hypno"]),
    wins_neither=dict(outline=S["wins_neither"], lookahead=L["wins_neither"]), first_action_shove=dict(outline=S["first_shove"], lookahead=L["first_shove"]),
    killers=dict(outline=S["killers"], lookahead=L["killers"]), median_turns=dict(outline=S["median_turns"], lookahead=L["median_turns"]),
    ghost_effect_points=gh, sessions=dict(outline=R["sessions"], lookahead=R["sessions_lookahead"]),
    ablation=ablation, hunt_lethal=dict(outline_every_8th=0.564, lookahead_every_400th=0.770),
    lookahead_sample="3,632 layouts (every 100th of 362,880); ablations every 400th (912 layouts); outline ablations every 4th layout"),
  previous=dict(verdict="NEEDS-FIXES", revision=0, bot_win_rates=P["bot_win_rates"], skill_expression=P["skill_expression"], skill_expression_outline=P["skill_expression_outline"],
                length=P["length"], solo_targets=prev),
  cards=cards, ambiguities=amb, problems=problems)
json.dump(out, open(os.path.join(HERE, "..", "playtest.json"), "w"), indent=1)
print("wrote playtest.json")
