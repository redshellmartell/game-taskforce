import sys, os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from game import Config, play
import bots as B, random
class Fixed(B.Random):
    def __init__(s,seed=0,f=None): super().__init__(seed); s.f=f
    def bid(s,st,p):
        h=st.hands[p]; return s.f(h,s.rng,st)
def mk(t):
    def f(h,rng,st):
        i=min(range(len(h)),key=lambda i:abs(h[i][1]-t)+rng.random()*.1); return i
    return f
pols={'low':lambda h,r,st:min(range(len(h)),key=lambda i:h[i][1]),
 'mid5':mk(5),'mid7':mk(7),'high':lambda h,r,st:max(range(len(h)),key=lambda i:h[i][1]),
 'pass':lambda h,r,st:None,
 'passthenhigh':lambda h,r,st:None if st.round<=5 else max(range(len(h)),key=lambda i:h[i][1]),
 'rand_nopass':lambda h,r,st:r.randrange(len(h))}
for nm in (6,5):
  for name,f in pols.items():
    cfg=Config(players=nm); wS=wR=0; N=800
    for s in range(N):
        kinds=[Fixed(s,f) if i==0 else B.Random(s+i) for i in range(nm)]
        r=play(cfg,kinds,s)
        for x in r['winners']:
            if x==0: wS+=1/len(r['winners'])
    print(nm,name,round(wS/N*100,1),"fair",round(100/nm,1))
