from game import Config
from run import match
for buoys,pts in [((1,1),0),((1,1),2),((1,1),3),((1,1),4),((1,2),0),((1,2),-3),((2,2),3)]:
    cfg=Config(buoys=buoys,second_pts=pts)
    out=[]
    for a in ["strategic","greedy","collector"]:
        r=match(cfg,a,a,2000,base=800000); out.append("%s %.1f"%(a,100*r["first_wins"]/2000))
    print(buoys,pts,out)
