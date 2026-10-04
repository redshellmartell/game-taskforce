import sys; import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from game import Config, play
import bots as B
for cv in (0.4,0.7,1.0,1.5):
  for nm in (6,5):
    cfg=Config(players=nm); wS=wR=0; N=600
    for s in range(N):
        kinds=[B.Strategic(s,cardval=cv) if i%2==0 else B.Random(s+i) for i in range(nm)]
        r=play(cfg,kinds,s)
        for x in r['winners']:
            if x%2==0: wS+=1/len(r['winners'])
            else: wR+=1/len(r['winners'])
    nS=(nm+1)//2; nR=nm//2
    print(cv,nm,round(wS/N/nS*100,1),round(wR/N/nR*100,1))
