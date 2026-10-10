import json, run as R
cells={"c4spin_x_draw2":dict(opening=0,shield_mode="spin",last_draw2=True),"c3big_x_cm1":dict(opening=0,shield_mode="big",mass_plus=1)}
out={}
for n,kw in cells.items():
    for ab in ("no-recall","comet-blind"):
        for k in (2,3,4):
            c=R.cell(R.mixed("strategic",ab,k),1000,kw,400+k)
            out[f"{n}|{ab}|{k}p"]=dict(margin=R.margin(c),giant_caps=c["cap_by_size"][4],comet_caps=c["cap_by_size"][0],recall=c["recall_per_game"])
            print(n,ab,k,out[f"{n}|{ab}|{k}p"],flush=True)
json.dump(out,open("results/sweep_abl.json","w"),indent=1)
