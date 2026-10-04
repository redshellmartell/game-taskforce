import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import game as G, bots as B
class Stop(Exception): pass
def desc(a):
    f=a["fx"]; par=a["params"]
    ps=",".join("%s=%s"%(k,(v["id"] if isinstance(v,dict) else getattr(v,"id",v))) for k,v in par.items() if k!="aug")
    return "%s %s [dmg%d sz%+d]"%(a["name"],ps,f["dmg"],f["size"])
class Me(B.Random):
    def __init__(self, plan): self.plan=plan; self.k=0; self.rng=__import__("random").Random(1)
    def nxt(self,what,opts):
        if self.k>=len(self.plan):
            print("DECISION",what); [print(" ",j,o) for j,o in enumerate(opts)]; raise Stop()
        v=self.plan[self.k]; self.k+=1; return v
    def choose_action(self, st, i, acts):
        p=st.P[i]
        if self.k>=len(self.plan):
            print("R%d me HP%d (%s) orbit %s tot %d | opp HP%d orbit %s tot %d | hand %s"%(st.round,p.hp,p.sid,[ (str(c) if c else '-') for c in p.orbit],G.total_size(st,i),st.P[1-i].hp,[ (str(c)+('+%d'%len(c.augs) if c.augs else '') if c else '-') for c in st.P[1-i].orbit],G.total_size(st,1-i),[c['id'] for c in p.hand]))
        v=self.nxt("act",[desc(a) for a in acts]+["END"])
        return acts[v] if v<len(acts) else None
    def pick(self, st, i, kind, opts, may=False):
        v=self.nxt("pick "+kind,[str(o[0])[:40] for o in opts]+["NONE"]); return opts[v][0] if v<len(opts) else None
    def discard_pick(self, st, i, pool):
        v=self.nxt("discard",[c["id"] for c in pool]); return pool[v]
def run(plan, seed=11):
    me=Me(plan); cfg=G.Config(2,stars=["ST04","ST05"],first=0,log=True)
    try:
        r=G.play(cfg,[me,B.Strategic(3)],seed); print("END",r["reason"],r["winner"],r["rounds"])
    except Stop: pass
if __name__=="__main__":
    run([int(x) for x in sys.argv[1:]])
