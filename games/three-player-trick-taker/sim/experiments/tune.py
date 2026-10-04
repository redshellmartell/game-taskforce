import sys,itertools;sys.path.insert(0,'..');sys.path.insert(0,'.')
from game import Game;import bots as B
def mixed(S,n=300):
    w=0;g_=0
    for j,p in enumerate(itertools.permutations([B.Random,B.Greedy,S])):
        for k in range(n):
            g=Game([m(10000*j+k*3+i) for i,m in enumerate(p)],10000*j+k).run()
            for i in g.winners:
                if p[i] is S: w+=1/len(g.winners)
                if p[i] is B.Greedy: g_+=1/len(g.winners)
    t=6*n;return round(w/t,3),round(g_/t,3)
def off(o):
    class O(B.Strategic):
        offset=o
    return O
for o in (-1,0,1): print('offset',o,mixed(off(o)))
class NoSwap(B.Strategic):
    def swap(self,R,seat,h9): return B.drop_lowest(h9,R.trump)
print('greedyswap',mixed(NoSwap))
class DCg(B.Strategic):
    def dc_play(self,R,seat,legal,trick,un):
        if trick: return B.win_cheap(legal,trick,R.trump) or B.lowest(legal)
        return B.highest(legal)
print('dc always grab',mixed(DCg))
