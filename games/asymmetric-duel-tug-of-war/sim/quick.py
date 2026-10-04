import sys; from game import play; import bots as B
w=[0,0]; ts=[]
for i in range(300):
    r=play((B.Strategic(i),B.Strategic(i+1)),i); w[r['winner']]+=1; ts.append(r['turns'])
print(w, sum(ts)/len(ts))
