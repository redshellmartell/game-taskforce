import sys,os,itertools
sys.path.insert(0,'..'); sys.path.insert(0,'.')
from run import sim
import bots as B
class GPlay(B.Strategic):
    name="s_greedyplay"
    play=B.Greedy.play
class GPlan(B.Strategic):
    name="s_greedyplan"
    plan=B.Greedy.plan; swap=B.Greedy.swap
class GSwap(B.Strategic):
    name="s_greedyswap"
    swap=B.Greedy.swap
class GPlanOnly(B.Strategic):
    name="s_greedyplanonly"
    plan=B.Greedy.plan
for cls in (B.Strategic,GPlay,GPlan,GSwap,GPlanOnly):
    tot=0
    for j,p in enumerate(itertools.permutations([B.Greedy,B.Random,cls])):
        r=sim(list(p),300,5000*(j+1)); tot+=r['byclass'][cls.name]
    print(cls.name, round(tot/6,3))
