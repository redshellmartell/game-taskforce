"""TEMPLATE game engine (the toy dice game Pig). Replace the rules with the game under test; keep the play() adapter shape.
Bot interface for this toy game: bot.roll_again(my_score, opp_score, turn_total) -> True to roll again, False to hold."""
import random

TARGET = 50
TURN_CAP = 400


def play(bots, seed):
    rng = random.Random(seed); score = [0, 0]; turn = 0; diffs = []
    while turn < TURN_CAP:
        p = turn % 2; total = 0
        while True:
            if bots[p].roll_again(score[p], score[1 - p], total) is False and total > 0: break
            d = rng.randint(1, 6)
            if d == 1: total = 0; break
            total += d
            if score[p] + total >= TARGET: break
        score[p] += total; turn += 1; diffs.append(score[0] - score[1])
        if score[p] >= TARGET:
            return dict(winner=p, turns=turn, capped=False, leaders=[0 if d > 0 else 1 if d < 0 else None for d in diffs])
    return dict(winner=None, turns=turn, capped=True, leaders=[0 if d > 0 else 1 if d < 0 else None for d in diffs])
