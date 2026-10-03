import sys; sys.path.insert(0,'..')
from run import sim
import bots as B
class A(B.Strategic):
    name="strategic"
    def swap(self,R,seat,h9): return B.drop_lowest(h9,R.trump)
class Bp(B.Strategic):
    name="strategic"
    def plan(self,R,seat,hand): return B.Greedy(0).plan(R,seat,hand)
class C(A):
    def plan(self,R,seat,hand): return B.Greedy(0).plan(R,seat,hand)
class D(C):  # + lead highest like greedy
    def play(self,R,seat,legal,trick):
        if not trick and self.want_win(R,seat,legal,trick): return B.highest(legal)
        return super().play(R,seat,legal,trick)
for name,c in (("greedyswap",A),("greedyplan",Bp),("both",C),("both+leadhigh",D)):
    r=sim([c,B.Greedy,B.Greedy],500,1); print(name,"seat0 win %.3f succ %.3f"%(r["seatwin"][0],r["success"]))
