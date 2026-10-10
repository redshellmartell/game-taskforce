import sys, json
sys.path.insert(0, '..')
import run as R, bots as B
out = {}
for n in (2, 4):
    w, rows = R.vs(n, B.NoBurst, B.Strategic, 2000, 600000 + n)
    out[n] = dict(rate=w, margin=(1.0 / n - w) * 100)
print(out); json.dump(out, open('e5_burst.json', 'w'))
