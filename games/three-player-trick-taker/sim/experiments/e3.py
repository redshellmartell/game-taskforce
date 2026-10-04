import sys,itertools
sys.path.insert(0,'.')
from run import sim
import bots as B
for bm in (2,3):
    tot={}
    for j,p in enumerate(itertools.permutations([B.Random,B.Greedy,B.Strategic])):
        r=sim(list(p),300,7000*(j+1),bmult=bm)
        for k,v in r['byclass'].items(): tot[k]=tot.get(k,0)+v/6
    print(bm,{k:round(v,3) for k,v in tot.items()}, round(r['lc'],2), round(r['early3'],2))
