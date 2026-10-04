import sys; sys.path.insert(0,'..')
from run import sim
import bots as B
for name,mk in (("RRR",[B.Random]*3),("GGG",[B.Greedy]*3),("SSS",[B.Strategic]*3),("SGG",[B.Strategic,B.Greedy,B.Greedy]),("GSS",[B.Greedy,B.Strategic,B.Strategic])):
    r=sim(mk,500,1)
    print(name,"succ %.3f"%r["success"],{t:(round(u,2),round(s,2)) for t,(u,s) in r["targ"].items()},"role",{k:round(v[0],2) for k,v in r["role"].items()},"seat0 %.3f"%r["seatwin"][0])
