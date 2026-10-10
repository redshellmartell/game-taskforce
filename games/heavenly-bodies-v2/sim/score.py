import json
r=json.load(open("results/sweep.json"))
band={"2p":(14,24),"3p":(18,30),"4p":(20,34)}; lnmax={"2p":.10,"3p":.10,"4p":.15}
def kp(x,k):
    s=x["share"]
    return dict(turns=band[k][0]<=x["turns"]<=band[k][1], caps=x["caps"]>=8, ln=x["ln"]<=lnmax[k], gap=x["gap"]<=5,
        run=(x["runaway"]<=.65) if k=="2p" else True, lc=x["lead"]>=2, svg=x["sv_greedy_pts"]>0, pat=all(.15<=s[p]<=.5 for p in s))
out=["| cell | 2p turns/min | 3p | 4p | caps 2/3/4 | LN% 2/3/4 | seat gap 2/3/4 | runaway 2p | lead chg 2p/3p/4p | strat-greedy pts 2/3/4 | pattern shares M/C/A 2p | KPIs in band of 24 |","|"+"---|"*12]
for n,v in r.items():
    tot=0; 
    for k in band: tot+=sum(kp(v[k],k).values())
    f=lambda key,fmt="{}":"/".join(fmt.format(v[k][key]) for k in band)
    sh=lambda k:"/".join("%.0f"%(100*v[k]["share"][p]) for p in("mass","const","align"))
    out.append(f"| {n} | "+" | ".join(f'{v[k]["turns"]:.1f} / {v[k]["minutes"]}' for k in band)+f" | {f('caps','{:.1f}')} | {'/'.join('%.0f'%(100*v[k]['ln']) for k in band)} | {f('gap','{:.1f}')} | {v['2p']['runaway']:.2f} | {f('lead','{:.1f}')} | {f('sv_greedy_pts','{:+.0f}')} | {sh('2p')} ; 3p {sh('3p')} ; 4p {sh('4p')} | {tot} |")
open("results/sweep_table.md","w").write("\n".join(out)); print("\n".join(out))
