"""Adds the playtester's judgement (verdict, problems, ambiguities) to ../playtest.json after run.py. Numbers come from run.py / experiments/exp-results.json."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); p = os.path.join(HERE, "..", "playtest.json")
pt = json.load(open(p)); ex = json.load(open(os.path.join(HERE, "experiments", "exp-results.json")))
pt["verdict"] = "NEEDS-FIXES"; pt["turn_cap_hits"] = 0
pt["round_10_end_rate"] = 0.75
for c in pt["cards"]:
    if c["name"] == "Sonar ping (spent)": c["flag"] = "no measurable value (E4: strategic without pinging wins 50.0%)"
    if c["name"] == "Torpedo hit": c["flag"] = "strong link to winning (0.33) but only ~1.9 hits per game"
pt["ambiguities"] = [
 "Does an unspent Sonar count toward 'lower score' for ping order and lead during the game? (sim: yes, 1 point each)",
 "Reef bounce clash: the other sub 'goes back' but has already entered its square; harmless today because the bouncer just emptied it, but the text reads as if it could matter",
 "A cancelled step (after a Mine): is the helm card still 'played' for cooling? (sim: yes, all 3 cards cool)",
 "Both subs targeting the same face-down card: collision says nothing is entered; is the card 'seen' by anyone? (sim: no)",
 "Tiebreak 'more Salvage cards' counts cards in pile after theft; Sonar excluded (sim assumption)",
 "Ping when both players could ping: only the first decider may; if they decline, the second may (sim follows this)"]
pt["problems"] = [
 dict(severity="high", problem="Runaway leader and too few lead changes",
      evidence="runaway-leader rate 0.79 (target <=0.65), lead changes 1.50 per game (target >=2); mirror strategic games 0.77 / 1.58. Final gap averages 7.4 points on 24 on the grid.",
      fix="Early fog flips decide the game and the only comeback (a torpedo hit, ~1.9 per game) is too rare. Try: hit steals the victim's highest card AND the victim cannot be hit next round; or a trailing player gets a free Helm card swap; or fewer Mines/more Salvage 1s so first flips swing less. Re-test with one change at a time."),
 dict(severity="medium", problem="Sonar ping has no measurable value",
      evidence="E4: strategic bot that never pings wins 50.0% against the normal strategic bot (1,000 games); only 1.4 pings per game.",
      fix="Make the ping reveal the whole plot order of one card more, or let the pinger see step 1 AND step 2; or drop the ping and make Sonar a simple 'peek at one face-down card' (check dead-card KPI)."),
 dict(severity="medium", problem="Simultaneous guessing adds little skill over plain route efficiency",
      evidence="Strategic beats greedy 71.8%, greedy beats random 84.8%; a strategic bot blind to the cooling rows loses only to 45.1% (E3), so reading the visible helm cards is worth ~5 points for a shallow bot. Most skill is exploration and safe routing.",
      fix="Cannot be judged from bots alone; human playtest should check whether reading the 6 visible cards feels meaningful. If not, make torpedo timing matter more (hits more often)."),
 dict(severity="medium", problem="Round 10 cap, not Salvage supply, ends 71-76% of games",
      evidence="Designer expected Salvage to run out in rounds 8-10; sim shows salvage left on the grid after round 10 in ~75% of strategic games. Mean 9.6 rounds, est. 14.8 min (OK).",
      fix="No length problem, but note a leader can safely coast and camp; consider cap 12 or fewer Mines only if lead changes stay low."),
 dict(severity="low", problem="Harbour camping not punished",
      evidence="E2: camper bot (ends rounds at home 3.6 of 10 rounds) wins 52.3% vs strategic (n=1000, +-3 points): not clearly dominant, but not worse.",
      fix="Watch in human play; if leaders turtle, limit Harbour safety to once per round pair."),
 dict(severity="low", problem="Torpedo spam is roughly fair, not dominant",
      evidence="E1: spammer (always plots T) wins 47.8% vs strategic. Hits per game 1.9; orthogonal-only range (E5) cuts hits to 1.1 per game with seat balance unchanged.",
      fix="None needed; keep 8-square range since hits are already rare.")]
pt["experiments"] = ex
json.dump(pt, open(p, "w"), indent=1)
print("verdict", pt["verdict"])
