import sys; sys.path.insert(0,'..')
from multiprocessing import Pool
from game import play
import bots as B
from collections import Counter
def one(a):
    name,n,s=a
    mk=B.MAKERS.get(name) or B.PERSONA.get(name)
    r=play([mk(s*7+i) for i in range(n)],s,n)
    S=r['stats']
    return r['pattern'][0],r['turns'],S['formed'],S['formed_survived'],S['full_formed'],S['full_survived'],S['captures']
if __name__=="__main__":
    with Pool(4) as p:
        for name in ("strategic","greedy","random","competitor","family"):
            for n in (2,3,4):
                rs=p.map(one,[(name,n,s) for s in range(60)])
                c=Counter(r[0] for r in rs)
                print(name,n,dict(c),"turns",sum(r[1] for r in rs)/60,"formed",sum(r[2] for r in rs),"surv",sum(r[3] for r in rs),"full",sum(r[4] for r in rs),sum(r[5] for r in rs),"caps",sum(r[6] for r in rs)/60)
