"""Builds ../playtest.json from results.json (headline run) plus a 30k-layout sample for card/win links."""
import itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from game import play, NAMES, TRICKS
import bots as B
R = json.load(open(os.path.join(HERE, "results.json")))
S, L, Rd, G = R["strategic"], R["lookahead"], R["random"], R["greedy"]
# win link: P(win | card beaten) - P(win | not beaten) and trick used vs not (when Ready at some point), outline bot, every 12th layout
cnt = {c: [0, 0, 0, 0] for c in range(1, 10)}; ucnt = {c: [0, 0, 0, 0] for c in TRICKS}; n = w = 0
for pm in itertools.islice(itertools.permutations(range(1, 10)), 0, 362880, 12):
    r = play(pm, (), B.Strategic()); n += 1; w += r.won; b = set(r.stats["beaten"]); u = set(r.stats["tricks"])
    for c in range(1, 10):
        cnt[c][0 if c in b else 2] += 1; cnt[c][1 if c in b else 3] += r.won
    for c in TRICKS:
        if c in r.stats["ever_ready"]: ucnt[c][0 if c in u else 2] += 1; ucnt[c][1 if c in u else 3] += r.won
f = lambda a, b: a / b if b else None
cards = []
for c in range(1, 10):
    nm = NAMES[c]; beaten = S["beaten"].get(nm, 0); sh = S["shoved"].get(nm, 0)
    d = dict(name=nm, played_rate=round(beaten, 3), shoved_rate=round(sh, 3))
    if c in TRICKS:
        t = S["trick_use_given_ready"].get(nm); tl = L["trick_use_given_ready"].get(nm)
        d["trick_use_given_ready_outline"] = t; d["trick_use_given_ready_lookahead"] = tl
        x = f(ucnt[c][1], ucnt[c][0]); y = f(ucnt[c][3], ucnt[c][2])
        d["win_correlation"] = round(x - y, 3) if x is not None and y is not None else None
    else:
        d["win_correlation"] = round(f(cnt[c][1], cnt[c][0]) - f(cnt[c][3], cnt[c][2]), 3) if cnt[c][0] and cnt[c][2] else None
    d["flag"] = None
    cards.append(d)
fl = {"Crow": "dead trick: Carry used in 0.15% of runs (outline) and never modelled by the lookahead bot; Thief is a pure tax",
      "Spider": "weak trick: Silk used in 0.3% of strong-bot runs, 25% outline; Spider is only a stepping stone",
      "Moth": "weak trick: Glow used in 0.5% of strong-bot runs (info is not worth a Ready trophy)",
      "Fox": "mandatory for strong play: Feint used in 100% of strong-bot runs where Ready"}
for d in cards:
    d["flag"] = fl.get(d["name"])
mean = L["mean_turns"]
problems = [
 dict(severity="high", problem="Win rate hinges on solver skill, not on the rules: outline bot wins 19.1%, a lookahead bot 80.8%; the 40-60% band sits in a 60-point gap between them",
      evidence="Exhaustive 362,880 layouts: outline 19.1%; lookahead (3,632 layouts, every 100th) 80.8%; random 0.0%; greedy 4.9%. Base Claws 3: outline 48.1%, lookahead 98.6%. Base Claws 1: 1.4% / 6.5%. A real player is somewhere between, so the true win rate is unknown",
      fix="Keep Claws 2 and get 3 or more human sessions before touching numbers; if humans track the outline bot, use Claws 3 with Hunt lethal (untested together) so the strong player is not at 99%"),
 dict(severity="high", problem="Outline strategic bot misses 4 of the designer's targets (win rate, median length, Feint share, killer spread)",
      evidence="Median 6 turns (target 7-12); wins using Feint 2.1% (target >=10%); only 3 cards cause over 5% of deaths (Fox 33%, Snake 11%, Hound 55%); the lookahead bot meets Feint 15.7%, Hypnotise 21.1%, neither 63%, median 9 turns, 8.3 min",
      fix="Treat the lookahead bot as the reference for variety targets; the outline loops (Shoves into the cell that holds the known Hound). A shove-target fix lifts it only to 24.7% in a 3,000-run check"),
 dict(severity="medium", problem="Ghost effect is far outside the 5-25 point target and uneven",
      evidence="Outline bot, one Ghost: Moth +0.0, Mouse +0.2, Spider +1.4, Rat +21, Hound +19, Snake +29, Crow +38, Fox +43, Owl +44 points. Ghost Moth/Mouse/Spider are nearly pointless; Ghost Owl/Fox/Crow nearly double the win rate",
      fix="Give low-card Ghosts a real effect (for example the Ghost grants a Ready trophy at setup) and cap the Owl/Fox/Crow Ghosts (Ghost Danger 2 rather than 0)"),
 dict(severity="medium", problem="Three tricks are close to dead and Carry is never tested by a strong bot",
      evidence="Strong-bot trick use when Ready: Moth 0.5%, Spider 0.3%, Crow 0 (not modelled); outline: Crow 0.15%. Target is 15%. Mouse 82%, Rat 86%, Snake 98%, Fox 100% in strong play",
      fix="Make Glow free of the Ready cost or let Silk also protect the Hound shove; rework Carry (swap plus a free Fight discount) and test it with a bot that models Carry"),
 dict(severity="medium", problem="Opening is a grind of Shoves in about 36% of layouts and the doorway can leave no safe Fight",
      evidence="Strategic bot's first action is a Shove in 35.7% of layouts (inside 20-60%) but the lookahead bot opens with a Shove in 90.9%; narrated play: three Shoves before the first Fight",
      fix="Consider a free Peek at one Dark card at setup, or start with 1 Ready trophy"),
 dict(severity="low", problem="Run length for a competent player is below the 10-minute target",
      evidence="Lookahead: mean %.1f turns, %.1f min (target 10, -17%%, inside the +/-20%% band); outline 6.4 min. Longest run 14 turns, no turn-cap hits in 700k runs" % (mean, L["est_minutes"]),
      fix="None needed unless human sessions run short; tally time and deliberation are not modelled"),
]
amb = ["Hound deep: the rules say you know where the Hound is, but only the swapped case gives you that (simulated that way); if it means always, the game gets much easier",
       "A Ghost still has to be fought to gain its trophy (uses an action); the design notes call it 'a free trophy'",
       "Scavenge can Ready a trick you already used this turn; implemented as still once per turn",
       "Hound lit by a Shove is hunted in the same turn's Phase 3 (implemented as written)",
       "Carry on a Lit card moving into the doorway or next to an empty space relights it; Lighting is derived from positions, so a face-down card can never stay face down there",
       "Strategic outline step 5 'unless you would then have 4+ Ready' and step 6 'leaves 1 Ready' are unclear on counting the new trophy (simulated: step 6 counts Ready after paying wounds, without the new card)"]
out = dict(verdict="NEEDS-FIXES", revision=0, games_simulated=362880 * 3 + 3632 + 20000 * 4,
  seat_win_rates={"1": 1.0}, seat_balance_gap=0.0,
  bot_win_rates={"random": Rd["win_rate"], "greedy": G["win_rate"], "strategic": S["win_rate"], "lookahead": L["win_rate"]},
  skill_expression=round((L["win_rate"] - Rd["win_rate"]) * 100, 1),
  skill_expression_outline=round((S["win_rate"] - Rd["win_rate"]) * 100, 1),
  length=dict(mean_turns=round(mean, 2), stdev=round(L["stdev_turns"], 2), estimated_minutes=round(L["est_minutes"], 1), target_minutes=10,
              outline_mean_turns=round(S["mean_turns"], 2), outline_minutes=round(S["est_minutes"], 1)),
  length_histogram=[dict(turns=t, games=c) for t, c in L["length_hist"]],
  ties=0.0, turn_cap_hits=0, lead_changes_mean=None, runaway_leader_rate=None,
  solo_notes="Seat balance, lead changes and runaway leader do not apply to a solo game.",
  solo_targets=dict(win_rate_band=[0.40, 0.60], outline_win_rate=S["win_rate"], lookahead_win_rate=L["win_rate"],
    wins_feint=dict(outline=S["wins_feint"], lookahead=L["wins_feint"]), wins_hypno=dict(outline=S["wins_hypno"], lookahead=L["wins_hypno"]),
    wins_neither=dict(outline=S["wins_neither"], lookahead=L["wins_neither"]),
    first_action_shove=dict(outline=S["first_shove"], lookahead=L["first_shove"]),
    killers=dict(outline=S["killers"], lookahead=L["killers"]), median_turns=dict(outline=S["median_turns"], lookahead=L["median_turns"]),
    ghost_effect_points={k: round((v - S["win_rate"]) * 100, 1) for k, v in R["ghost"].items()},
    sessions=dict(outline=R["sessions"], lookahead=R["sessions_lookahead"]),
    lookahead_sample="3,632 layouts (every 100th of 362,880)"),
  cards=cards, ambiguities=amb, problems=problems)
json.dump(out, open(os.path.join(HERE, "..", "playtest.json"), "w"), indent=1)
print("wrote playtest.json")
