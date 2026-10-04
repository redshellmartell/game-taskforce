import sys,itertools,json;sys.path.insert(0,'..');sys.path.insert(0,'.')
import run as RN, bots as B
res={}
for v in ("double_final","cleanloot","flat"):
    m=RN.sim([B.Strategic]*3,2000,100000,variant=v)
    byc={B.Random.name:0,B.Greedy.name:0,B.Strategic.name:0}
    for j,p in enumerate(itertools.permutations([B.Random,B.Greedy,B.Strategic])):
        r=RN.sim(list(p),334,10000*(j+1),variant=v)
        for k,x in r["byclass"].items(): byc[k]+=x*334
    res[v]=dict(lc=m["lc"],early3=m["early3"],gap=(max(m["seatwin"])-min(m["seatwin"]))*100,success=m["success"],role={k:round(x[0],2) for k,x in m["role"].items()},mixed={k:round(x/2004,3) for k,x in byc.items()})
    print(v,res[v])
json.dump(res,open('experiments/variants.json','w'),indent=1)
