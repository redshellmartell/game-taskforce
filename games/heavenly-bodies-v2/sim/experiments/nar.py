import sys; sys.path.insert(0,'..')
from game import play
import bots as B
n=int(sys.argv[1]); r=play([B.MAKERS['strategic'](i) for i in range(n)],int(sys.argv[2]),n,log=True)
L=r['st'].log
print(len(L),r['turns'],r['pattern'],r['winner'])
print("\n".join(L[:int(sys.argv[3])]))
print("...\n".join(L[-4:]))
