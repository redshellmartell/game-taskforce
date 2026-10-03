import time, sys
from game import Game
import bots as B
t=time.time()
for i in range(300):
    g=Game([B.Strategic(i),B.Greedy(i),B.Random(i)],i).run()
print(time.time()-t, g.scores, g.winners)
g=Game([B.Strategic(1)]*1+[B.Greedy(1),B.Random(1)],5,log=True).run(); print("\n".join(g.log[:12]))
