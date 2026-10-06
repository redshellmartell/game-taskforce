"""Rev-1 extra configurations. Usage: python3 exp.py"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
from multiprocessing import Pool
import run as R
N = 600
CONFIGS = [("X1 strategic mirror, ping reveals 3 steps", "strategic", "strategic", {"ping_steps": 3}),
           ("X2 strategic(A) v noping, ping reveals 3 steps", "strategic", "noping", {"ping_steps": 3}),
           ("X3 spammer(A) v strategic", "spammer", "strategic", {}),
           ("X4 strategic mirror, 8-round cap", "strategic", "strategic", {"max_rounds": 8})]
out = {}
with Pool(4) as pool:
    for i, (label, a, b, cfg) in enumerate(CONFIGS):
        rows = R.run_pair(a, b, N, cfg, base=700000 + 10000 * i, pool=pool); s = R.summ(rows, a)
        out[label] = {k: round(v, 3) for k, v in s.items()}; print(label, out[label])
json.dump(out, open(os.path.join(HERE, "exp-results.json"), "w"), indent=1)
