"""5 extra configurations. Usage: python3 exp.py"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from multiprocessing import Pool
import run as R
N = 1000
CONFIGS = [("E1 spammer(A) v strategic", "spammer", "strategic", {}),
           ("E2 camper(A) v strategic", "camper", "strategic", {}),
           ("E3 blind-to-cooling(A) v strategic", "blind", "strategic", {}),
           ("E4 noping(A) v strategic", "noping", "strategic", {}),
           ("E5 strategic mirror, torpedo orthogonal only", "strategic", "strategic", {"torp8": False})]
out = {}
with Pool(4) as pool:
    for i, (label, a, b, cfg) in enumerate(CONFIGS):
        rows = R.run_pair(a, b, N, cfg, base=900000 + 10000 * i, pool=pool); s = R.summ(rows, a)
        pg = [p for r in rows for p in r["pg"]]
        extra = dict(hits=sum(p["hits"] for p in pg) / len(rows), fired=sum(p["fired"] for p in pg) / len(rows),
                     home_a=sum(p["home"] for p in pg if p["bot"] == a) / len(rows), lc=s["lc"])
        out[label] = {**{k: round(v, 3) for k, v in s.items()}, **{k: round(v, 2) for k, v in extra.items()}}
        print(label, out[label])
json.dump(out, open(os.path.join(HERE, "exp-results.json"), "w"), indent=1)
