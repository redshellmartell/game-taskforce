"""Dead Reckoning headline run. Usage: python3 run.py [games_per_pairing=2000]. Writes ../playtest.json and results.json."""
import sys, os, json, statistics, math
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from game import Config, play
import bots as B
ALL = {c.name: c for c in (B.Random, B.Greedy, B.Strategic, B.Spammer, B.Camper, B.Blind, B.NoPing, B.Mid, B.NoTorp, B.NoMiddle)}
CFGKEYS = ("torp8", "max_rounds", "harbour_safe", "zoned", "ping_steps")

def one(args):
    a, b, k, seed, cfgd = args
    first_is_a = (k % 2 == 0)
    names = (a, b) if first_is_a else (b, a)
    bots = (ALL[names[0]](seed * 2 + 1), ALL[names[1]](seed * 2 + 2))
    r = play(Config(**cfgd), bots, seed); g = r["game"]; st = g.s
    h = g.history; rs = g.round_scores; w = r["winner"]
    sg = [x for x in ((d > 0) - (d < 0) for d in h) if x]
    lc = sum(1 for x, y in zip(sg, sg[1:]) if x != y)
    mid = rs[(len(rs) - 1) // 2] if rs else 0
    early = None if (mid == 0 or w is None) else int((mid > 0) == (w == 0))
    pg = []
    for seat in (0, 1):
        pg.append(dict(bot=names[seat], seat=seat, win=1.0 if w == seat else 0.5 if w is None else 0.0,
            salv=[st.stats["taken%d" % v][seat] for v in (1, 2, 3)], mines=st.stats["mines"][seat], reef=st.stats["reef_found"][seat],
            sonar=st.stats["taken6"][seat], T=st.stats["Tplays"][seat], hits=st.stats["hits"][seat], fired=st.stats["fired"][seat],
            ping=st.stats["pings"][seat], home=st.stats["harbour_rounds"][seat], blocked=st.stats["blocked"][seat],
            score=r["scores"][seat]))
    return dict(rounds=r["rounds"], lc=lc, early=early, tie=w is None, capped=r["capped"], coll=st.stats["collisions"], pg=pg,
                r1=(g.r1 if hasattr(g, 'r1') else 0), c1=st.stats.get('coll_r1', 0), winseat=w, diff=abs(r["scores"][0] - r["scores"][1]))

def run_pair(a, b, n, cfgd=None, base=0, pool=None):
    cfgd = cfgd or {}
    jobs = [(a, b, k, base + k, cfgd) for k in range(n)]
    return pool.map(one, jobs, chunksize=20) if pool else list(map(one, jobs))

def summ(rows, a):
    """Win rate of bot `a` and general stats."""
    n = len(rows); pw = [p["win"] for r in rows for p in r["pg"] if p["bot"] == a]
    s1 = [0.5 if r["winseat"] is None else float(r["winseat"] == 0) for r in rows]
    return dict(n=n, a_win=sum(pw) / len(pw) if pw else 0, seat1=sum(s1) / n, rounds=statistics.mean(r["rounds"] for r in rows),
                ties=sum(r["tie"] for r in rows) / n, runaway=(lambda e: sum(e)/len(e) if e else 0)([r["early"] for r in rows if r["early"] is not None]), capped=sum(r["capped"] for r in rows) / n, lc=statistics.mean(r["lc"] for r in rows))

def corr(xs, ys):
    n = len(xs); mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs)); sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy) if sx and sy else 0.0

def main(n=2000):
    pairs = [("strategic", "random"), ("strategic", "greedy"), ("greedy", "random"), ("strategic", "strategic"), ("greedy", "greedy"), ("random", "random"),
             ("strategic", "mid"), ("mid", "greedy"), ("mid", "random"), ("mid", "mid")]
    res = {}; allrows = []
    with Pool(4) as pool:
        for i, (a, b) in enumerate(pairs):
            rows = run_pair(a, b, n, base=100000 * (i + 1), pool=pool); res["%s-v-%s" % (a, b)] = (a, b, rows); allrows += rows
    out = {}
    for key, (a, b, rows) in res.items():
        s = summ(rows, a); out[key] = {k: round(v, 4) for k, v in s.items()}
    # seat balance from mirror matches
    mir = [r for key in ("strategic-v-strategic", "greedy-v-greedy", "random-v-random") for r in res[key][2]]
    seat1 = sum(0.5 if r["winseat"] is None else float(r["winseat"] == 0) for r in mir) / len(mir)
    seat_by = {k: out[k]["seat1"] for k in ("strategic-v-strategic", "greedy-v-greedy", "random-v-random")}
    gap = abs(seat1 - 0.5) * 2 * 100
    # bot win rates: overall share across all non-mirror games
    bw = {}
    for nm in ("random", "greedy", "strategic"):
        w = [p["win"] for r in allrows for p in r["pg"] if p["bot"] == nm]; bw[nm] = sum(w) / len(w)
    sr = out["strategic-v-random"]["a_win"]; skill = (sr - (1 - sr)) * 100
    sg = out["strategic-v-greedy"]["a_win"]
    rounds = [r["rounds"] for r in allrows]
    strat = [r for key in ("strategic-v-strategic", "strategic-v-greedy", "strategic-v-random") for r in res[key][2]]
    srounds = [r["rounds"] for r in strat]; mean_r = statistics.mean(srounds)
    est = round(mean_r * 85 / 60 + 1, 1)
    hist = {}
    for r in srounds: hist[r] = hist.get(r, 0) + 1
    lcm = statistics.mean(r["lc"] for r in strat)
    early = [r["early"] for r in strat if r["early"] is not None]; runaway = sum(early) / len(early)
    ties = sum(r["tie"] for r in strat) / len(strat); cap = sum(r["capped"] for r in strat)
    pgs = [p for r in strat for p in r["pg"]]
    win = [p["win"] for p in pgs]
    feats = {"Salvage 1": lambda p: p["salv"][0], "Salvage 2": lambda p: p["salv"][1], "Salvage 3": lambda p: p["salv"][2],
             "Mine": lambda p: p["mines"], "Reef": lambda p: p["reef"], "Sonar (taken)": lambda p: p["sonar"],
             "Sonar ping (spent)": lambda p: p["ping"], "Torpedo (played)": lambda p: p["T"], "Torpedo hit": lambda p: p["hits"],
             "Harbour (rounds ended home)": lambda p: p["home"]}
    cards = []
    for nm, f in feats.items():
        xs = [f(p) for p in pgs]; pr = sum(1 for x in xs if x > 0) / len(xs); c = corr(xs, win)
        flag = None
        if nm.startswith("Salvage"): flag = None
        elif pr < 0.1: flag = "rarely used"
        elif abs(c) >= 0.3: flag = "strong link to winning"
        cards.append(dict(name=nm, played_rate=round(pr, 3), win_correlation=round(c, 3), flag=flag, per_game=round(statistics.mean(xs), 2)))
    extra = dict(hits_per_game=statistics.mean(p["hits"] for p in pgs) * 2, mines_per_game=statistics.mean(p["mines"] for p in pgs) * 2,
                 fired_per_game=statistics.mean(p["fired"] for p in pgs) * 2, pings_per_game=statistics.mean(p["ping"] for p in pgs) * 2,
                 collisions_per_game=statistics.mean(r["coll"] for r in strat), blocked_per_game=statistics.mean(p["blocked"] for p in pgs) * 2,
                 reef_found_per_game=statistics.mean(p["reef"] for p in pgs) * 2, mean_final_gap=statistics.mean(r["diff"] for r in strat))
    def r1eff(rows):
        d = [(r["r1"] > 0) == (r["winseat"] == 0) for r in rows if r["r1"] != 0 and r["winseat"] is not None]
        return sum(d) / len(d) if d else 0
    r1 = r1eff(strat); r1coll = statistics.mean(1 if r["c1"] > 0 else 0 for r in strat)
    abl = {}
    with Pool(4) as pool:
        for i, (a, b, cf) in enumerate([("strategic", "blind", {}), ("strategic", "noping", {}), ("strategic", "notorp", {}), ("strategic", "nomiddle", {}),
                                        ("strategic", "camper", {}), ("strategic", "strategic", {"zoned": False})]):
            rows = run_pair(a, b, n, cf, base=900000 + 100000 * i, pool=pool)
            s = summ(rows, a)
            abl[b + ("-v1deal" if cf else "")] = dict(full_win=round(s["a_win"], 3), ablated_win=round(1 - s["a_win"], 3), runaway=round(s["runaway"], 3), lc=round(s["lc"], 2), rounds=round(s["rounds"], 2))
    mixed = [r for key in ("strategic-v-mid", "mid-v-greedy", "mid-v-random", "strategic-v-greedy", "strategic-v-random") for r in res[key][2]]
    json.dump(dict(pairings=out, seat1_mirror=seat_by, extra=extra, cards=cards, ablations=abl, r1_leader_wins=r1, r1_collision_rate=r1coll), open(os.path.join(HERE, "results.json"), "w"), indent=1)
    pt = dict(verdict="PENDING", revision=1, mid_vs=dict(strategic_v_mid=out["strategic-v-mid"]["a_win"], mid_v_greedy=out["mid-v-greedy"]["a_win"], mid_v_random=out["mid-v-random"]["a_win"]), ablations=abl, r1_leader_wins=round(r1, 3), r1_collision_rate=round(r1coll, 3), games_simulated=len(allrows), seat_win_rates={"1": round(seat1, 3), "2": round(1 - seat1, 3)},
              seat_balance_gap=round(gap, 1), bot_win_rates={k: round(v, 3) for k, v in bw.items()}, skill_expression=round(skill, 1),
              strategic_vs_greedy=round(sg, 3),
              length=dict(mean_turns=round(mean_r, 2), stdev=round(statistics.pstdev(srounds), 2), estimated_minutes=est, target_minutes=15),
              length_histogram=[dict(turns=k, games=v) for k, v in sorted(hist.items())], ties=round(ties, 4), turn_cap_hits=cap,
              lead_changes_mean=round(lcm, 2), runaway_leader_rate=round(runaway, 3), cards=cards, ambiguities=[], problems=[], extra={k: round(v, 2) for k, v in extra.items()})
    json.dump(pt, open(os.path.join(HERE, "..", "playtest.json"), "w"), indent=1)
    print("games %d | seat1 mirror %.3f (gap %.1f pts) %s" % (len(allrows), seat1, gap, seat_by))
    for k, v in out.items(): print("%-24s A win %.3f  rounds %.2f  ties %.3f runaway %.2f capped %.2f  lc %.2f" % (k, v["a_win"], v["rounds"], v["ties"], v["runaway"], v["capped"], v["lc"]))
    print("skill (S-v-R gap) %.1f pts | S-v-G %.3f | est %.1f min | runaway %.3f | lead changes %.2f | caps %d" % (skill, sg, est, runaway, lcm, cap))
    print({k: round(v, 2) for k, v in extra.items()})
    print("r1 leader wins %.3f | r1 collision rate %.3f" % (r1, r1coll)); print("ablations", abl)
    for kk in ("strategic-v-mid", "mid-v-greedy", "mid-v-random", "mid-v-mid"): print(kk, out[kk])
    for c in cards: print("%-28s played %.2f corr %+.2f per game %.2f %s" % (c["name"], c["played_rate"], c["win_correlation"], c["per_game"], c["flag"] or ""))

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2000)
