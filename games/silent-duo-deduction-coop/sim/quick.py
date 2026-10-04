import sys, time
from game import Game, play
import bots as B
def run(cls, n=2, N=300, fog=8, **kw):
    w = 0; t = 0; sc = 0; extra = {}
    for s in range(N):
        g = Game(n, fog, s)
        play(g, [cls(s * 7 + k, **kw) for k in range(n)])
        w += g.win; t += g.turns
    return w / N, t / N
if __name__ == "__main__":
    t = time.time()
    for name, c in B.TIERS.items(): print(name, run(c))
    print(time.time() - t)
