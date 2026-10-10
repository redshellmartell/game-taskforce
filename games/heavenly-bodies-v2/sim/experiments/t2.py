import sys; sys.path.insert(0,'..')
from game import play, orb_str
import bots as B
r=play([B.MAKERS['strategic'](i) for i in range(2)],1,2,log=True)
print({k:v for k,v in r['stats'].items()})
print("\n".join(r['st'].log[:40]))
