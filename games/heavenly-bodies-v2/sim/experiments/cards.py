import sys,json; sys.path.insert(0,'..')
from multiprocessing import Pool
import run as R
if __name__=="__main__":
    with Pool(4) as pool:
        out={}
        for k in (2,3):
            rows=R.run_games(["strategic"]*k,400,777+k,{},pool)
            w={s:[0,0] for s in range(1,6)}; l={s:[0,0] for s in range(1,6)}
            for r in rows:
                if r['winner'] is None: continue
                for p,f in enumerate(r['final']):
                    t=w if p==r['winner'] else l
                    for s in range(1,6): t[s][0]+=f.count(s); t[s][1]+=1
            out[k]={s:dict(win=w[s][0]/max(1,w[s][1]),lose=l[s][0]/max(1,l[s][1])) for s in range(1,6)}
        json.dump(out,open('../results/cards.json','w'),indent=1); print(json.dumps(out)[:900])
