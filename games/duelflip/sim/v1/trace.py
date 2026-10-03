import sys, random
from game import Config, State, SPECIES
import bots as B
N="CSUAKL"
def c(x): return "%s%d"%(N[x[0]],x[1])
def trace(seed, bots):
    cfg=Config(); st=State(cfg, random.Random(seed))
    while st.deck:
        p=st.player; bot=bots[p]; st.pile=[]; bust=False; first=True
        print("T%d P%d(buoys %d) river=[%s] deck=%d haul=%d/%d"%(st.turn+1,p+1,st.buoys[p],",".join(map(c,st.river)),len(st.deck),st.hauls_value(0),st.hauls_value(1)))
        while st.deck:
            if not first and not bot.keep_flipping(st,p): break
            card=st.deck.pop(); first=False
            if card[1] in st.river_values():
                st.discard.append(card)
                if st.buoys[p]>0 and bot.use_buoy(st,p,card):
                    st.buoys[p]-=1; print("   flip %s CLASH -> LIFEBUOY (pile %s)"%(c(card),",".join(map(c,st.pile)))); break
                bust=True; print("   flip %s CLASH -> BUST, gives %s (value %d)"%(c(card),",".join(map(c,st.pile)) or "nothing",sum(v for _,v in st.pile)))
                for x in st.pile: st.river.remove(x); st.haul[1-p].append(x)
                break
            st.river.append(card); st.pile.append(card); print("   flip %s"%c(card))
        if not bust:
            if len(st.river)==1: st.haul[p].append(st.river.pop()); print("   bank 1 card")
            else:
                i=bot.leave(st,p); keep=st.river[i]
                tk=[x for j,x in enumerate(st.river) if j!=i]; st.haul[p]+=tk; st.river=[keep]
                print("   bank %s, leave %s"%(",".join(map(c,tk)),c(keep)))
        st.turn+=1; st.player=1-p
    print("FINAL scores",st.score(0),st.score(1),"hauls",st.hauls_value(0),st.hauls_value(1),"buoys",st.buoys)
    for q in (0,1):
        print(" P%d species counts:"%(q+1),[sum(1 for s,_ in st.haul[q] if s==k) for k in range(6)])
trace(int(sys.argv[1]), (B.Strategic(1),B.Greedy(2)) if sys.argv[2]=="sg" else (B.Strategic(1),B.Strategic(2)))
