import sys; sys.path.insert(0,'/home/user/game-taskforce/games/silent-duo-deduction-coop/sim')
import game as G, bots as B, run
from collections import Counter
# diag: at Honest 2p F8 trim turns, was an offer legal?
c=Counter()
orig=G.Game.step
def step(self,a):
    if a[0]=="trim":
        c["trim"]+=1
        if any(x[0]=="offer" for x in self.legal(self.cur)): c["trim_with_offer"]+=1
    c["turn"]+=1
    return orig(self,a)
G.Game.step=step
run.team(B.Honest,2,2000,8)
print(dict(c), c["trim_with_offer"]/c["trim"])
G.Game.step=orig
# Beacon off: patch fog move
import types
src=open('/home/user/game-taskforce/games/silent-duo-deduction-coop/sim/game.py').read().replace("if self.deck:\n                        mv","if False:\n                        mv")
ns={}; exec(compile(src,'g2','exec'),ns)
run.Game=ns['Game']; run.play=ns['play']
for fog in (8,12):
  for cls in (B.Honest,B.Greedy):
    print("beacon-off",cls.name,fog,run.summ(run.team(cls,2,2000,fog))["win"])
