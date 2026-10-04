import sys,itertools
sys.path.insert(0,'.')
from game import Game
import bots as B
from collections import defaultdict
st=defaultdict(lambda:[0,0,0,0])
for j,p in enumerate(itertools.permutations([B.Greedy,B.Random,B.Strategic])):
  for k in range(300):
    g=Game([m(k*3+i) for i,m in enumerate(p)],j*1000+k).run()
    for r in g.rec:
      for role,seat in (("P",r["planner"]),("S",r["safe"]),("D",r["dc"])):
        e=st[(p[seat].name,role)]; e[0]+=1; e[1]+=r["pts"][seat]; e[2]+=r["tricks"][seat]; e[3]+=r["ok"]
for k in sorted(st): n,a,b,c=st[k]; print(k, "pts %.2f tricks %.2f ok %.2f"%(a/n,b/n,c/n))
