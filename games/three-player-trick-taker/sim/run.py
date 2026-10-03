"""Headline simulation for Split the Take. Usage: python3 run.py [N=2000]. Writes ../playtest.json and results.json."""
import itertools, json, os, statistics, sys
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from game import Game
import bots as B

SLUG_DIR = os.path.abspath(os.path.join(HERE, ".."))
MIN_PER_ROUND = 1 + 7 * 17.5 / 60.0      # rules.md: ~1 min admin + 7 tricks at 15-20 s

def credit(g):
    return {i: (1.0 / len(g.winners) if i in g.winners else 0.0) for i in range(3)}

def sim(makers, n, seed0, **kw):
    """makers: list of 3 bot classes, one per seat. Returns aggregate dict."""
    A = defaultdict(float); targ = defaultdict(lambda: [0, 0]); trump = defaultdict(lambda: [0, 0])
    role_pts = defaultdict(list); heat_n = 0; rounds = 0; tgt_pts = defaultdict(list); nt_pts = defaultdict(list)
    heat_pts = []; nonheat_lead_pts = []
    lcs = []; early3 = early2 = n3 = n2 = 0; ties = 0; scores = []; margins = []
    seatwin = [0.0] * 3; byclass = defaultdict(float)
    for k in range(n):
        g = Game([m(seed0 + k * 3 + i) for i, m in enumerate(makers)], seed0 + k, **kw).run()
        c = credit(g)
        for i in range(3): seatwin[i] += c[i]; byclass[makers[i].name] += c[i]
        if len(g.winners) > 1: ties += 1
        seq = [x for x in g.lead_seq if x is not None]
        lcs.append(sum(1 for a, b in zip(seq, seq[1:]) if a != b))
        if len(g.lead_seq) >= 3 and g.lead_seq[2] is not None: n3 += 1; early3 += c[g.lead_seq[2]]
        if len(g.lead_seq) >= 2 and g.lead_seq[1] is not None: n2 += 1; early2 += c[g.lead_seq[1]]
        scores += g.scores; sr = sorted(g.scores)[::-1]; margins.append(sr[0] - sr[1])
        A["ruffs"] += g.ruffs; A["tricks"] += g.tricks_played; A["dcs"] += sum(g.dc_wins)
        for r in g.rec:
            rounds += 1; targ[r["target"]][0] += 1; targ[r["target"]][1] += r["ok"]
            tk = "NT" if r["trump"] is None else "suit"; trump[tk][0] += 1; trump[tk][1] += r["ok"]
            role_pts["Planner"].append(r["pts"][r["planner"]]); role_pts["Safecracker"].append(r["pts"][r["safe"]]); role_pts["Double-Crosser"].append(r["pts"][r["dc"]])
            tgt_pts[r["target"]].append(r["pts"][r["planner"]] + r["pts"][r["safe"]] - 0)  # crew total points
            nt_pts[tk].append(r["pts"][r["planner"]])
            if r["heat"] is not None:
                heat_n += 1; heat_pts.append((r["pts"][r["heat"]]))
        A["decisions"] += sum(g.decisions); A["turns"] += sum(g.turns)
    allp = [x for v in role_pts.values() for x in v]; mu = statistics.mean(allp); sd = statistics.pstdev(allp)
    return dict(n=n, seatwin=[x / n for x in seatwin], byclass={k: v / n for k, v in byclass.items()}, ties=ties / n,
                lc=statistics.mean(lcs), early3=early3 / max(1, n3), early2=early2 / max(1, n2),
                success=sum(v[1] for v in targ.values()) / rounds, targ={t: (v[0] / rounds, v[1] / v[0]) for t, v in sorted(targ.items())},
                trump={k: (v[0] / rounds, v[1] / v[0]) for k, v in trump.items()},
                role={k: (statistics.mean(v), (statistics.mean(v) - mu) / sd) for k, v in role_pts.items()},
                heat_rate=heat_n / rounds, heat_pts=statistics.mean(heat_pts) if heat_pts else 0, mean_round_pts=mu,
                score_mean=statistics.mean(scores), margin=statistics.mean(margins), ruff=A["ruffs"] / A["tricks"],
                dcrate=A["dcs"] / rounds, rounds=rounds)

def main(N=2000):
    out = {}
    # 1. mixed table: random / greedy / strategic in all 6 seat permutations
    perms = list(itertools.permutations([B.Random, B.Greedy, B.Strategic])); per = N // 6 + 1
    byc = defaultdict(float); tot = 0
    for j, p in enumerate(perms):
        r = sim(list(p), per, 10000 * (j + 1))
        for k, v in r["byclass"].items(): byc[k] += v * per
        tot += per
    out["mixed"] = {k: v / tot for k, v in byc.items()}; out["mixed_games"] = tot
    # 2. skill: one strategic vs two random, strategic rotated through seats
    sr = defaultdict(float); tot = 0; per = N // 3 + 1
    for j in range(3):
        mk = [B.Random] * 3; mk[j] = B.Strategic
        r = sim(mk, per, 50000 + 7000 * j); sr["strategic"] += r["seatwin"][j] * per
        sr["random_each"] += (sum(r["seatwin"]) - r["seatwin"][j]) / 2 * per; tot += per
    out["skill"] = {k: v / tot for k, v in sr.items()}; out["skill_games"] = tot
    gr = 0.0
    for j in range(3):
        mk = [B.Random] * 3; mk[j] = B.Greedy
        gr += sim(mk, per, 60000 + 7000 * j)["seatwin"][j] * per
    out["skill"]["greedy"] = gr / tot
    # 3. mirror: strategic x3 -> seats, length, lead changes, contract stats
    base = sim([B.Strategic] * 3, N, 100000); out["mirror"] = base
    # 4. extra configurations (max 5)
    ex = {}
    ex["no_heat"] = sim([B.Strategic] * 3, N, 100000, heat=False)
    class Fixed5(B.Strategic):
        name = "fixed5"
        def plan(self, R, seat, hand): return super().plan(R, seat, hand)[0], 5
    class Off(B.Strategic):
        off = 0
    def off(o):
        class O(B.Strategic):
            name = "off%+d" % o; offset = o
        return O
    class AlwaysWin(B.Strategic):
        name = "dc_always_win"
        def want_win(self, R, seat, legal, trick):
            return True if R.role(seat) == "D" else super().want_win(R, seat, legal, trick)
    for key, cls in (("fixed5", Fixed5), ("offset-1", off(-1)), ("offset+1", off(1)), ("dc_always_win", AlwaysWin)):
        r = sim([cls, B.Strategic, B.Strategic], N, 200000)
        ex[key] = {"seat0_win": r["seatwin"][0], "success": r["success"], "dcrate": r["dcrate"]}
    out["experiments"] = ex
    json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1, default=str)
    return out

def summarise(out, N):
    b = out["mirror"]; sk = out["skill"]; mixed = out["mixed"]
    gap_seat = (max(b["seatwin"]) - min(b["seatwin"])) * 100
    skill = (sk["strategic"] - sk["random_each"]) * 100
    est = 6 * MIN_PER_ROUND
    print("games: mixed %d, skill %d, mirror %d, experiments 5x%d" % (out["mixed_games"], out["skill_games"], b["n"], b["n"]))
    print("seat win rates (S,S,S): %s gap %.1f pts" % ([round(x, 3) for x in b["seatwin"]], gap_seat))
    print("bot win rates (R/G/S table): %s" % {k: round(v, 3) for k, v in mixed.items()})
    print("skill: strategic %.3f vs each random %.3f  gap %.1f pts" % (sk["strategic"], sk["random_each"], skill))
    print("greedy vs two random: %.3f" % sk["greedy"])
    print("length: fixed 42 tricks / 6 rounds, est %.1f min" % est)
    print("ties %.4f  lead changes %.2f  early leader (after R3) wins %.3f (after R2 %.3f)" % (b["ties"], b["lc"], b["early3"], b["early2"]))
    print("contract success %.3f  DC success %.3f; by target: %s" % (b["success"], b["dcrate"], {t: (round(u, 2), round(s, 2)) for t, (u, s) in b["targ"].items()}))
    print("role pts/round: %s" % {k: (round(v[0], 2), round(v[1], 2)) for k, v in b["role"].items()})
    print("heat in %.2f of rounds; holder avg pts %.2f (round avg %.2f); mean final %.1f margin %.1f; ruff rate %.2f" % (b["heat_rate"], b["heat_pts"], b["mean_round_pts"], b["score_mean"], b["margin"], b["ruff"]))
    print("no-heat: gap %.1f lc %.2f early3 %.3f" % ((max(out["experiments"]["no_heat"]["seatwin"]) - min(out["experiments"]["no_heat"]["seatwin"])) * 100, out["experiments"]["no_heat"]["lc"], out["experiments"]["no_heat"]["early3"]))
    for k, v in out["experiments"].items():
        if k != "no_heat": print("  exp %s: seat0 win %.3f success %.3f dcrate %.3f" % (k, v["seat0_win"], v["success"], v["dcrate"]))

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    out = main(N); summarise(out, N)
    import finalize; finalize.build(out, N)
