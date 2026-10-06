import sys
sys.path.insert(0,'/home/user/game-taskforce/games/four-player-partnership-climber/sim'); sys.path.insert(0,'/home/user/game-taskforce/tools/sim-kit')
import simkit, game, bots as B
class R2(B.Reader):
    def __init__(s,seed,hold=True,**k): super().__init__(seed,**k); s.hold=hold
    def choose(s,g,me,legal,leading):
        if not leading and not s.hold:
            # emulate: no high-single hold
            old=s.kind; s.kind=True
            try: return super().choose(g,me,legal,leading)
            finally: s.kind=old
        return super().choose(g,me,legal,leading)
def run(name,mk,n=600):
    rows=simkit.run_match(game.play,[mk,mk,B.Greedy,B.Greedy],n,5)
    s=simkit.summarize(rows,4); w=s['maker_win_rates']; print(name,'reader',round((w[0]+w[1])/2,3),'greedy',round((w[2]+w[3])/2,3))
run('current',B.Reader)
run('nohold',lambda s:R2(s,hold=False))
run('thr1.1(no pass for partner)',lambda s:R2(s,hold=False,thr=1.1))
run('thr.6 ropeearly',lambda s:R2(s,hold=False,rope_early=True))
run('relay_blind nohold',lambda s:R2(s,hold=False,relay_blind=True))
print('--- attempt 2')
class R3(B.Reader):
    def __init__(s,seed,greedylead=True,nopass=False,**k): super().__init__(seed,**k); s.gl=greedylead; s.g_=B.Greedy(seed)
    def lead(s,g,me,legal):
        if s.gl: return s.g_.choose(g,me,legal,True)
        return super().lead(g,me,legal)
run('greedy lead + partner pass',lambda s:R3(s,kind=True))
run('greedy lead + partner pass thr.8',lambda s:R3(s,kind=True,thr=0.8))
run('greedy lead, thr 1.1',lambda s:R3(s,kind=True,thr=1.1))
run('reader lead, thr 1.1 kind',lambda s:R3(s,greedylead=False,kind=True,thr=1.1))
print('--- attempt 3')
class R4(R3):
    def choose(s,g,me,legal,leading):
        if not leading:
            P=s.P(g); h=g.holder
            if P[h]>=0.99 and g.size[h]<=5 and not any(pl[1]==g.size[me] for pl in legal): return None   # let a KNOWN partner who is close to out keep the trick
            old=s.thr0; s.thr0=1.5
            try: return super().choose(g,me,legal,leading)
            finally: s.thr0=old
        return super().choose(g,me,legal,leading)
run('known partner near out only (greedy lead)',lambda s:R4(s,kind=True))
run('same, reader lead',lambda s:R4(s,greedylead=False,kind=True))
run('known partner any size',lambda s:R3(s,kind=True,thr=0.99))
