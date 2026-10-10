"""Heavenly Bodies simulation, revision 1. Usage: python3 run.py [games=2000] [part]   (part: all | head | abl)
Prints a compact summary (<40 lines); writes sim/results.json and ../playtest.json. Fixed seeds."""
import itertools, json, math, os, random, statistics, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import game as G
import bots as B

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MIN_PER_TURN = 1.0      # estimate: one player-turn ~1 minute at the table; +3 min setup (same estimate as revision 0)
SETUP_MIN = 3.0
S, Rn, Gr = B.Strategic, B.Random, B.Greedy


def one(cfg, bots, seed):
    r = G.play(cfg, bots, seed); st = r["st"]
    h = st.history; mid = h[len(h) // 2] if h else None
    w = r["winner"]
    return dict(w=w, reason=r["reason"], rounds=r["rounds"], turns=r["turns"], capped=r["capped"], lc=st.lead_changes, mid=mid,
                wt=(st.P[w].turns if w is not None else None), stats=st.stats, pc={k: sorted(v) for k, v in st.pc.items()},
                cp=dict(st.card_plays), first_dead=list(st.first_dead), cancel_by=list(st.cm_cancel_by), stars=[p.sid for p in st.P],
                tp=list(st.turn_plays), mull=st.mulligans)


def batch(n, mk, cfgf, seed0):
    return [one(cfgf(k), mk(k), seed0 + k) for k in range(n)]


def share(rows, f): return sum(1 for r in rows if f(r)) / max(1, len(rows))
def mean(xs): xs = list(xs); return sum(xs) / len(xs) if xs else float("nan")
def sd(xs): xs = list(xs); return statistics.pstdev(xs) if len(xs) > 1 else 0.0


def wilson(k, n, z=1.96):
    if n == 0: return (0, 0)
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - m) / d, (c + m) / d)


def paths(rows):
    n = len(rows); cm = sum(1 for r in rows if r["reason"] == "cm"); st = sum(1 for r in rows if r["reason"] == "star")
    lo, hi = wilson(cm, max(1, cm + st))
    return dict(n=n, cm=cm / n, star=st / n, cm_ci=[round(lo, 3), round(hi, 3)], cap=share(rows, lambda r: r["capped"]), turns=mean(r["turns"] for r in rows))


def cmsum(rows):
    ann = sum(r["stats"]["cm_announce"] for r in rows); can = sum(r["stats"]["cm_cancel"] for r in rows)
    by = [x for r in rows for x in r["cancel_by"]]
    return dict(announces=ann / len(rows), cancel_share=can / max(1, ann), cancel_by_opp=sum(1 for x in by if x == "opp") / max(1, len(by)), cm_win_per_announce=sum(1 for r in rows if r["reason"] == "cm") / max(1, ann))


def cardstats(rows, nplayers):
    out = {}
    for cid in G.CARDS:
        pg = []
        for r in rows:
            if r["w"] is None: continue
            for pl in range(nplayers): pg.append((cid in r["pc"].get(pl, []), r["w"] == pl))
        a = [w for p, w in pg if p]; b = [w for p, w in pg if not p]
        out[cid] = dict(played=mean(1 if cid in r["cp"] else 0 for r in rows), link=(mean(a) - mean(b)) if a and b else 0.0, per_player=len(a) / max(1, len(pg)))
    return out


def vs(n, A, Bc, N, seed0, **cfg):
    """Bot class A (one seat, rotated) against n-1 copies of Bc. Returns A's win rate and fair share 1/n."""
    wins = 0; rows = []
    for k in range(N):
        seat = k % n
        bs = [Bc(k * 11 + j) for j in range(n)]; bs[seat] = A(k * 11 + 99)
        r = one(G.Config(n, first=0, **cfg), bs, seed0 + k); rows.append(r)
        wins += (r["w"] == seat)
    return wins / N, rows


def head(N):
    res = {}
    # ---- 2p strategic mirror (seat gap, length, lead changes, runaway, cards)
    rows = batch(N, lambda k: [S(k), S(k + 1)], lambda k: G.Config(2, first=0), 10000)
    res["mirror2"] = dict(**paths(rows), seat=[share(rows, lambda r: r["w"] == 0), share(rows, lambda r: r["w"] == 1)],
                          lc=mean(r["lc"] for r in rows), turns_sd=sd(r["turns"] for r in rows),
                          runaway=mean(1 if r["mid"] == r["w"] else 0 for r in rows if r["mid"] is not None and r["w"] is not None),
                          hist={t: sum(1 for r in rows if r["turns"] == t) for t in sorted({r["turns"] for r in rows})},
                          cmev=cmsum(rows), recycles=mean(r["stats"].get("recycles", 0) for r in rows), mulligans=mean(r["mull"] for r in rows),
                          rot_coll=mean(r["stats"].get("rot_collisions", 0) for r in rows), coll=mean(r["stats"]["collisions"] for r in rows),
                          caps=sum(1 for r in rows if r["capped"]))
    res["cards2"] = cardstats(rows, 2)
    # ---- reference bots, 2p round robin (alternate seats)
    ids = ["random", "greedy", "strategic"]; rr = {}
    for a, b in itertools.combinations(ids, 2):
        A, Bc = B.STANDARD[a], B.STANDARD[b]
        w = 0; pr = []
        for k in range(N):
            if k % 2 == 0: bs = [A(k), Bc(k + 1)]; wa = 0
            else: bs = [Bc(k + 1), A(k)]; wa = 1
            r = one(G.Config(2, first=0), bs, 20000 + k); pr.append(r); w += (r["w"] == wa)
        rr[a + "_v_" + b] = w / N
    res["pairs"] = rr
    avg = {"random": mean([rr["random_v_greedy"], rr["random_v_strategic"]]), "greedy": mean([1 - rr["random_v_greedy"], rr["greedy_v_strategic"]]),
           "strategic": mean([1 - rr["random_v_strategic"], 1 - rr["greedy_v_strategic"]])}
    res["bot_avg"] = avg; res["spread"] = max(avg.values()) - min(avg.values())
    # ---- path split by count, strategic mirror
    res["split"] = {}; res["len"] = {}
    for n in (3, 4, 5, 6):
        rs = batch(N, lambda k: [S(k * 7 + j) for j in range(n)], lambda k: G.Config(n, first=0), 40000 + n * 3000)
        res["split"][n] = dict(**paths(rs), seat=[share(rs, lambda r, s=s: r["w"] == s) for s in range(n)], lc=mean(r["lc"] for r in rs), cmev=cmsum(rs),
                               runaway=mean(1 if r["mid"] == r["w"] else 0 for r in rs if r["mid"] is not None and r["w"] is not None))
        if n == 4: res["cards4"] = cardstats(rs, 4)
    res["split"][2] = {k: res["mirror2"][k] for k in ("n", "cm", "star", "cm_ci", "turns", "seat", "lc", "runaway")}
    # ---- Star round-robin at 2p (each unordered pair, seats alternate)
    sid = sorted(G.STARS); tot = {s: [0, 0] for s in sid}
    for a, b in itertools.combinations(sid, 2):
        for k in range(100):
            order = [a, b] if k % 2 == 0 else [b, a]
            r = one(G.Config(2, stars=order, first=0), [S(k), S(k + 1)], 50000 + k + 1000 * sid.index(a) + 37 * sid.index(b))
            tot[a][1] += 1; tot[b][1] += 1
            if r["w"] is not None: tot[order[r["w"]]][0] += 1
    res["stars2"] = {s: dict(win=v[0] / v[1], hp=G.STARS[s]["hp"]) for s, v in tot.items()}
    # Star table at 4p: each Star in a random 4-Star table (stars random, strategic bots), count wins per Star
    t4 = {s: [0, 0] for s in sid}; rows4 = []
    for k in range(N):
        rg = random.Random(70000 + k); pick = rg.sample(sid, 4)
        r = one(G.Config(4, stars=pick, first=0), [S(k * 3 + j) for j in range(4)], 70000 + k)
        for j, s in enumerate(pick):
            t4[s][1] += 1
            if r["w"] == j: t4[s][0] += 1
    res["stars4"] = {s: dict(win=v[0] / max(1, v[1]), n=v[1]) for s, v in t4.items()}
    # ---- dead cards per 7-card hand on an empty board
    hands = 4000; dead_hist = {}; no_co = 0
    for h in range(hands):
        st = G.State(G.Config(2, first=0), h); G.setup(st, [S(0), S(1)])
        p = st.P[0]; p.hand = [st.deck.pop() for _ in range(7)]; p.entered = 0
        d = sum(1 for c in p.hand if not G.gen_one(st, 0, c)); dead_hist[d] = dead_hist.get(d, 0) + 1
        no_co += (not any(c["type"] == "CO" for c in p.hand))
    res["dead"] = dict(per_hand=sum(k * v for k, v in dead_hist.items()) / hands, no_co=no_co / hands, hist={k: v / hands for k, v in sorted(dead_hist.items())})
    res["turn_plays"] = dict(t1_two=share(rows, lambda r: dict(r["tp"])[1] == 2), t1_zero=share(rows, lambda r: dict(r["tp"])[1] == 0))
    return res


def abl(N):
    res = {}
    # (a)-(d) bot ablations at 2p and 4p: ablated bot against full strategic; margin = fair share minus win rate, in points
    for name in ("always_cw", "ignore_north", "no_recycle", "no_mull"):
        res[name] = {}
        for n in (2, 4):
            w, rows = vs(n, B.ABL[name], S, N, 100000 + n * 500, )
            res[name][n] = dict(rate=w, margin=(1.0 / n - w) * 100, ci=[round(x, 3) for x in wilson(round(w * N), N)])
    # (e) Star ability off: the Star (ability on) against the same Star (ability off), 2p; and 1 on vs 3 off at 4p
    res["ability"] = {}
    for sid_ in ("ST08", "ST10", "ST11", "ST12"):
        out = {}
        for n in (2, 4):
            on = 0
            for k in range(N):
                seat = k % n
                off = set(range(n)) - {seat}
                r = one(G.Config(n, stars=[sid_] * n, first=0, abil_off=off), [S(k * 5 + j) for j in range(n)], 150000 + k)
                on += (r["w"] == seat)
            out[n] = dict(on=on / N, margin=(on / N - 1.0 / n) * 100)
        res["ability"][sid_] = out
    # (f) lever: flat 15 versus scaled
    res["flat15"] = {}
    for n in (2, 3, 4, 6):
        rs = batch(N, lambda k: [S(k * 7 + j) for j in range(n)], lambda k: G.Config(n, first=0, thr=15), 200000 + n * 3000)
        res["flat15"][n] = paths(rs)
    return res


def exps(N):
    """Extra configurations (budget 5): E1 ST12 free -1 off; E2 ST11 active+reclaim damage off; E3 threshold 16 at 5-6p;
    E4 CM-first vs damage-first sensitivity at 2p; E5 the same at 4p."""
    res = {}
    base = {}
    for n in (2, 4):
        rs = batch(N, lambda k: [S(k * 7 + j) for j in range(n)], lambda k: G.Config(n, first=0), 300000 + n * 3000)
        base[n] = paths(rs)
    for name, ff in (("E1_st12_free_off", {"st12"}), ("E2_st11_off", {"st11"})):
        res[name] = {}
        for n in (2, 4):
            sidn = name.split("_")[1].upper()
            win = 0; n_pl = 0; rows = []
            for k in range(N):
                seat = k % n
                rg = random.Random(310000 + k); others = rg.sample([x for x in sorted(G.STARS) if x != sidn], n - 1)
                order = others[:seat] + [sidn] + others[seat:]
                r = one(G.Config(n, stars=order, first=0, feat_off=ff), [S(k * 5 + j) for j in range(n)], 310000 + k); rows.append(r)
                win += (r["w"] == seat)
            # same seeds with the feature on
            win_on = 0; rows_on = []
            for k in range(N):
                seat = k % n
                rg = random.Random(310000 + k); others = rg.sample([x for x in sorted(G.STARS) if x != sidn], n - 1)
                order = others[:seat] + [sidn] + others[seat:]
                r = one(G.Config(n, stars=order, first=0), [S(k * 5 + j) for j in range(n)], 310000 + k); rows_on.append(r)
                win_on += (r["w"] == seat)
            res[name][n] = dict(star_win_on=win_on / N, star_win_off=win / N, fair=1.0 / n, paths_on=paths(rows_on), paths_off=paths(rows))
    res["E3_thr16_5_6p"] = {}
    for n in (5, 6):
        for lab, th in (("17", None), ("16", 16)):
            rs = batch(N, lambda k: [S(k * 7 + j) for j in range(n)], lambda k: G.Config(n, first=0, thr=th), 400000 + n * 3000)
            res["E3_thr16_5_6p"]["%dp_thr%s" % (n, lab)] = paths(rs)
    res["E4_priorities"] = {}
    for n in (2, 4):
        for lab, cl in (("cm_first", B.CMFirst), ("dmg_first", B.DmgFirst)):
            rs = batch(N, lambda k: [cl(k * 7 + j) for j in range(n)], lambda k: G.Config(n, first=0), 500000 + n * 3000)
            res["E4_priorities"]["%dp_%s_mirror" % (n, lab)] = paths(rs)
        w, rows = vs(n, B.CMFirst, B.DmgFirst, N, 520000 + n)
        res["E4_priorities"]["%dp_cm_first_beats_dmg_first_rate" % n] = w
    res["base"] = base
    return res


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    part = sys.argv[2] if len(sys.argv) > 2 else "all"
    t0 = time.time(); out = {}
    fn = os.path.join(HERE, "results_%s.json" % part)
    if part in ("all", "head"): out["head"] = head(N)
    if part in ("all", "abl"): out["abl"] = abl(N)
    if part in ("all", "exp"): out["exp"] = exps(N)
    out["elapsed"] = time.time() - t0; out["N"] = N
    json.dump(out, open(fn, "w"), indent=1, default=str)
    print("wrote", fn, "elapsed %.0fs" % out["elapsed"])
