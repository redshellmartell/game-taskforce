import sys, json, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import game as G, bots as B, run as R
S = B.Strategic
def deck(drop, add, n=1):
    ids = [dict(c) for c in G.DATA["cards"]]
    out = []
    for c in ids:
        out.append(dict(G.CARDS[add]) if c["id"] in drop else c)
    return out
variants = {
 "E1_first_player_draws_1": dict(first_draw=1),
 "E1b_first_player_draws_0": dict(first_draw=0),
 "E2_plus6_dmg": dict(deck_ids=deck(["AE48","AE59","AE60","AE55","AE57","AE45"], "AE23")),
 "E3_minus6_dmg": dict(deck_ids=deck(["AE23","AE26","AE33","AE35","AE30","AE37"], "AE47")),
}
out = {}
for name, kw in variants.items():
    modes = (2,) if name.startswith("E1") else (2, 4)
    for n in modes:
        rs = []
        for k in range(2000):
            cfg = G.Config(n, first=0, **kw)
            rs.append(R.one(cfg, [S(k * 5 + j) for j in range(n)], 90000 + k))
        ps = R.path_summary(rs)
        out["%s_%dp" % (name, n)] = dict(cm=round(ps["cm_share"], 3), star=round(ps["star_share"], 3), rounds=round(ps["rounds_all"], 2),
                                          star_rounds=round(ps["star_rounds"], 2), cm_rounds=round(ps["cm_rounds"], 2),
                                          seat1=round(R.share(rs, lambda r: r["w"] == 0), 3))
        print(name, n, out["%s_%dp" % (name, n)], flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "exp_results.json"), "w"), indent=1)
