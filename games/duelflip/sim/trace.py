import sys
from game import Config, play
from run import mk
seed = int(sys.argv[1]); a = sys.argv[2]; b = sys.argv[3]
r = play(Config(log=True), (mk(a, seed), mk(b, seed + 1)), seed)
print("\n".join(r["st"].log)); print("scores", r["scores"], "turns", r["turns"], "buoys", r["st"].buoys)
