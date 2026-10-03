import sys; sys.path.insert(0,'..')
from run import sim
import bots as B
class CrewGreedy(B.Strategic):
    name="strategic"
    def want_win(self,R,seat,legal,trick):
        if R.role(seat)=="D": return super().want_win(R,seat,legal,trick)
        return True
class DCGreedy(B.Strategic):
    name="strategic"
    def want_win(self,R,seat,legal,trick):
        if R.role(seat)=="D": return True
        return super().want_win(R,seat,legal,trick)
class Soft(B.Strategic):   # crew ducks only on the last 2 tricks when need<=0
    name="strategic"
    def want_win(self,R,seat,legal,trick):
        if R.role(seat)!="D" and R.target-R.crew<=0 and R.remaining>2: return True
        return super().want_win(R,seat,legal,trick)
for name,c in (("crewGreedy",CrewGreedy),("dcGreedy",DCGreedy),("soft",Soft),("base",B.Strategic)):
    r=sim([c,B.Greedy,B.Greedy],500,1); print(name,"seat0 win %.3f succ %.3f"%(r["seatwin"][0],r["success"]))
