import sys, os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from game import Config, play
import bots as B
class Bank(B.Strategic):
    bank=0
    def bid(s,st,p):
        if st.round<=s.bank: return None
        return super().bid(st,p)
for bank in (0,3,5,7):
 for cv in (0.0,0.4):
  for nm in (6,5):
    cfg=Config(players=nm); wS=wR=0; N=600
    for s in range(N):
        kinds=[Bank(s,cardval=cv,bank=bank) if i%2==0 else B.Random(s+i) for i in range(nm)]
        r=play(cfg,kinds,s)
        for x in r['winners']:
            if x%2==0: wS+=1/len(r['winners'])
            else: wR+=1/len(r['winners'])
    print(bank,cv,nm,round(wS/N/((nm+1)//2)*100,1),round(wR/N/(nm//2)*100,1))
