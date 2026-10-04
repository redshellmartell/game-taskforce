import sys, time
from game import Config, play
import bots as B
t=time.time()
cfg=Config(players=6)
w={'S':0,'R':0,'G':0}
for s in range(300):
    bs=[B.Strategic(s),B.Random(s+1),B.Greedy(s+2),B.Strategic(s+3),B.Random(s+4),B.Greedy(s+5)]
    r=play(cfg,bs,s)
    for x in r['winners']: w['SRG'[ [0,1,2,0,1,2][x] ]=='S' and 'S' or 'RG'[[0,1,2,0,1,2][x]==2] ]+=1/len(r['winners'])
print(w,time.time()-t, r['scores'], r['st'].hype_counts())
