import sys; sys.path.insert(0,'..')
from game import Config
from run import match
for ex in (3,):
    cfg=Config(extra=ex)
    for a,b in [("strategic:low","strategic:smart"),("strategic:high","strategic:smart")]:
        R=match(cfg,a,b,2000,base=500000)
        print("hurdle bait+%d"%ex,a,"v",b,"%.1f"%(100*R["a"]/2000),"claim %.2f turns %.1f"%(R["S"]["claims"]/max(1,R["S"]["claim_tries"]),sum(R["turns"])/2000))
    R=match(cfg,"strategic","strategic",2000,base=1)
    print("mirror seat1 %.1f halfway-leader %.1f"%(100*R["first"]/2000,100*R["el"]/R["eln"]))
