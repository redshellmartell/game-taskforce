"""TEMPLATE bots. Every game needs at least: random, greedy and strategic (different strengths), plus one ablated bot per
advertised twist (it ignores exactly one rule and must lose by 5+ points; lesson L1). Makers are callables seed -> bot."""
import random


class Random:
    def __init__(self, seed): self.r = random.Random(seed)
    def roll_again(self, me, opp, total): return self.r.random() < 0.7


class Greedy:                                   # holds at a fixed total
    def __init__(self, seed, hold=20): self.hold = hold
    def roll_again(self, me, opp, total): return total < self.hold


class Strategic:                                # holds lower when ahead, higher when behind
    def __init__(self, seed, ignore_opponent=False): self.ignore = ignore_opponent
    def roll_again(self, me, opp, total):
        if me + total >= 50: return False
        hold = 20 if self.ignore else (16 if me > opp + 10 else 26 if me < opp - 10 else 21)
        return total < hold


MAKERS = {"random": Random, "greedy": Greedy, "strategic": Strategic}
ABLATED = {"ignore-opponent-score": lambda seed: Strategic(seed, ignore_opponent=True)}   # one entry per twist
