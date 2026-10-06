import sys, statistics as S
import os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import game, bots as B
N = 2000
def run(a, b):
    tw = 0; lc = []; r3 = 0
    for i in range(N):
        r = game.play((B.ALL[a](i), B.ALL[b](i + 7919)), 700000 + i); tw += r["winner"] == 0; r3 += r["rounds"] <= 3
    return round(tw / N, 3), round(r3 / N, 3)
def cfg(label, mod):
    saved = (dict(game.T_DECK), dict(game.W_DECK)); mod()
    print(label, {p: run(p, p) for p in ("random", "greedy", "strategic", "plus")}, flush=True)
    game.T_DECK.clear(); game.T_DECK.update(saved[0]); game.W_DECK.clear(); game.W_DECK.update(saved[1])
cfg("whisper4", lambda: game.W_DECK.update({"The Whisper": (1, 4, "hush")}))
cfg("gold_purse5", lambda: game.T_DECK.update({"Gold Purse": (3, 5, "")}))
