from game import Config, play
import bots as B
from run import match
class GL(B.Greedy):
    def __init__(s,seed=0,mode="low"): super().__init__(seed); s.mode=mode
    def leave(s,st,p):
        r=range(len(st.river))
        if s.mode=="low": return min(r,key=lambda i:st.river[i][1])
        if s.mode=="high": return max(r,key=lambda i:st.river[i][1])
        if s.mode=="rand": return s.rng.choice(list(r))
        if s.mode=="bait": return max(r,key=lambda i:(st.deck_count(st.river[i][1]),-st.river[i][1]))
for m in ["high","rand","bait"]:
    B.ALL["g_"+m]=(lambda m:(lambda seed=0:GL(seed,m)))(m)
    r=match(Config(),"g_"+m,"greedy",2000,base=1)
    print("greedy leave=%s vs greedy leave=low: win %.1f%%"%(m,100*r["a_wins"]/2000))
# dead turns and leftover value stats (greedy mirror)
dead=0;turns=0;lv=[];
for i in range(500):
    res=play(Config(),(B.Greedy(i),B.Greedy(i+1)),i); turns+=res["turns"]
    st=res["st"]
print("greedy mirror turns/game",turns/500)
# count zero-gain bust turns
import game
dead=0;tot=0
for i in range(500):
    cfg=Config(); 
    orig=B.Greedy
    res=play(cfg,(B.Strategic(i),B.Strategic(i+1)),i)
    tot+=res["turns"]
print("strategic mirror turns", tot/500)
