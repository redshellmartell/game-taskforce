import sys,time,os
sys.path.insert(0,'..'); 
from game import play
import bots as B
for n in (2,3,4):
    t=time.time(); res=[]
    for s in range(20):
        r=play([B.MAKERS['strategic'](s*3+i) for i in range(n)],s,n)
        res.append(r)
    print(n,(time.time()-t)/20,[ (r['turns'],r['winner'],r['pattern']) for r in res[:6]])
