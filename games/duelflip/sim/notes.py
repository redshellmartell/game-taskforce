"""Text for playtest.json that a person (the playtester) wrote after reading the numbers.
Everything here is transcribed from ../playtest-report.md (v2 rules re-test); the numbers are not.
"""

VERDICT = "NEEDS-FIXES"
REVISION = 1  # one revision loop done: rules v1 -> v2

# Human-play estimate from the narrated games in the report ("about 12 minutes for a human").
ESTIMATED_MINUTES = 12
# The brief asks for 10-15 minutes; the target used here is the middle of that range.
TARGET_MINUTES = 12.5

AMBIGUITIES = [
    "River with only 1 card at banking: section 4 says at least 2, but it can be 1 (deck runs out after the first flip, or a Lifebuoy is spent on a second-flip clash). Interpreted: you take the single card.",
    "Safe scout when the deck runs dry: if every remaining card matches the river the scout redraws until the deck is empty with an empty pile, and the game ends (consistent with section 5).",
    "Refund counting: the card you leave counts toward the 4 cards, and the refund only applies if the Lifebuoy was spent. Interpreted by the playtester; not stated in the rules.",
    "Multiple leftovers: only 0 or 1 leftover can exist, so the 'other leftovers stay in the river' wording in section 4 is dead text.",
    "Lifebuoy on a bait clash: spending it keeps your pile and you must bank the bait. Allowed, but not stated.",
    "Tiebreaker: equal score, then more cards, then the second player. Assumed.",
]

# Ranked problems from the report. Severity: report's Medium -> medium, Low-Med and Low -> low.
PROBLEMS = [
    {"severity": "medium", "problem": "Bait/leave decision is solved by 'leave your lowest card'",
     "evidence": "Leaving high wins 17-24% and random 31-36% against leave-lowest; the best clever leave rule gains only +2 to +3 points. The answer is 'lowest' about 3 turns in 4.",
     "fix": "Make a bait hit pay more (bait owner also takes a card from the opponent's pile, or the pile counts double), then re-run experiments.py section A. Target: leave-lowest under 60% against a smart leaver."},
    {"severity": "medium", "problem": "Species bonus decides only about 5% of games",
     "evidence": "Flips the winner in 4.8% of games at bonus 8 (v1: about 4% at 5). The species-aware leave rule scores 45-47% against plain lowest, so chasing species costs more than it gains.",
     "fix": "Score the bonus per card of margin (for example +3 per card ahead) or raise it to 12-15, then re-run section E. Target: swings 10%+ of games."},
    {"severity": "low", "problem": "Pushing deep is not rewarded and the Lifebuoy refund is rarely used",
     "evidence": "Pusher targets 4 to 20 all win 35-40% against strategic. Refund happens 0.56 times per game. Refund at 3 re-tilts seat 1 to 55.5%.",
     "fix": "Move the refund to 3 cards with seat 2 +4, or drop the refund and keep a one-shot Lifebuoy."},
    {"severity": "low", "problem": "1-card busts feel like small taxes",
     "evidence": "10-17% of turns; average bust pile 5.6 points, none reach 15.",
     "fix": "Optionally make the Lifebuoy free when the pile is one card."},
    {"severity": "low", "problem": "Mild snowball",
     "evidence": "The leader after one third of the game wins 66-70%. Unchanged from v1.",
     "fix": "None needed; acceptable."},
    {"severity": "low", "problem": "Random bots give seat 1 only 48%",
     "evidence": "Small over-correction from the +3 compensation; no bot is further than 2 points from fair.",
     "fix": "Keep +3 (+2 is an alternative)."},
]

# The playtester's judgement of the three advertised twists (report, questions 2, 6 and 7). They are design
# elements rather than individual cards, so they are listed in the "cards" section of playtest.json.
# win_correlation is null for all three: a plain correlation would be confounded (holding more cards means
# more points), so the effect is described in words instead.
CARD_FLAGS = {
    "Species majority bonus": "inert: changes the winner in only about 5% of games at bonus 8",
    "Lifebuoy refund": "inert: refunded about 0.56 times per game and changes no measurable outcome",
    "Bait (leave one card)": "dominated: leaving the lowest card is the right choice about 3 turns in 4",
}
