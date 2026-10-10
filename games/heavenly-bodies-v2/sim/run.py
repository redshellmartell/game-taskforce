"""Heavenly Bodies v2 playtest runner. Usage: python3 run.py <section> [N] ; sections: headline skill ablate variants all
Writes results to sim/results/<section>.json; `python3 run.py report` prints a compact summary and writes ../playtest.json."""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools", "sim-kit"))
from multiprocessing import Pool
import simkit
from game import play
import bots as B

OUT = os.path.join(HERE, "results"); os.makedirs(OUT, exist_ok=True)
TARGET_MINUTES = 12


def maker(spec):
    if spec in B.MAKERS: return B.MAKERS[spec]
    if spec in B.ABLATED: return B.ABLATED[spec]
    return B.PERSONA[spec]


def one(a):
    specs, n, i, seed, kw = a
    k = len(specs)
    order = [(j + i) % k for j in range(k)]
    bots = [maker(specs[order[s]])(seed + i * 7 + s) for s in range(k)]
    r = play(bots, seed + i, k, **kw)
    S = r["stats"]; st = r["st"]
    fin = [sorted(c[1] for c in o if c) for o in st.orbits]
    return dict(winner=r["winner"], turns=r["turns"], capped=r["capped"], leaders=r["leaders"], order=order, pattern=r["pattern"],
                long_night=r["long_night"], stats={k2: v for k2, v in S.items()}, final=fin)


def run_games(specs, n, seed=0, kw=None, pool=None):
    args = [(specs, len(specs), i, seed, kw or {}) for i in range(n)]
    return pool.map(one, args, chunksize=8)


def digest(rows, players):
    s = simkit.summarize(rows, players)
    N = len(rows)
    tot = lambda key: sum(r["stats"][key] for r in rows)
    pats = {}
    for r in rows:
        if r["winner"] is None: pats["tie"] = pats.get("tie", 0) + 1; continue
        p = r["pattern"][0] if r["pattern"][0] in ("longnight",) else "+".join(r["pattern"])
        pats[p] = pats.get(p, 0) + 1
    # first-listed pattern attribution (mass > const > align) for pattern wins
    wins_pat = {"mass": 0, "const": 0, "align": 0}
    for r in rows:
        if r["winner"] is not None and r["pattern"][0] in wins_pat:
            for x in r["pattern"]: wins_pat[x] += 1 / len(r["pattern"])
    spins = tot("spins") or 1
    out = dict(summary=s, n=N, long_night_rate=round(sum(r["long_night"] for r in rows) / N, 4),
               pattern_wins=pats, pattern_wins_split=wins_pat,
               captures_per_game=round(tot("captures") / N, 2), ties_per_game=round(tot("ties") / N, 2),
               crash_spin_share=round(tot("crash_spins") / spins, 3), other_spin_share=round(tot("other_spins") / spins, 3),
               other_crash_share=round(tot("other_crash") / max(1, tot("other_spins")), 3),
               self_crash_share=round(tot("self_crash") / max(1, tot("self_spins")), 3),
               formed_per_game=round(tot("formed") / N, 2), formed_survival=round(tot("formed_survived") / max(1, tot("formed")), 4),
               full_per_game=round(tot("full_formed") / N, 2), full_survival=round(tot("full_survived") / max(1, tot("full_formed")), 4),
               rebound_per_game=round(tot("rebounds") / N, 2), recall_per_game=round(tot("recalls") / N, 2),
               deep_take_per_draw=round(tot("deep_takes") / max(1, tot("draws")), 3),
               turns_exceed_deck_bound=sum(1 for r in rows if r["turns"] > {2: 43, 3: 38, 4: 33}[players]),
               mean_turns=s["length"]["mean_turns"])
    # does the longnight winner correlate with early leader / total
    return out


def sweep_players(pool, spec_fn, n, kw=None, seed=0):
    res = {}
    for k in (2, 3, 4):
        rows = run_games(spec_fn(k), n, seed + k * 100000, kw, pool)
        res[str(k)] = digest(rows, k)
        res[str(k)]["makers"] = spec_fn(k)
        res[str(k)]["maker_rates"] = res[str(k)]["summary"]["maker_win_rates"]
    return res


def section(name, N):
    t0 = time.time()
    with Pool(4) as pool:
        if name == "headline":
            out = sweep_players(pool, lambda k: ["strategic"] * k, N)
            # card/size stats from the 2p..4p mirror: size counts in winner vs others final orbit
            out["_note"] = "all-strategic mirror"
        elif name == "skill":
            out = {}
            out["strategic_v_random"] = sweep_players(pool, lambda k: ["strategic"] + ["random"] * (k - 1), N, seed=11)
            out["greedy_v_random"] = sweep_players(pool, lambda k: ["greedy"] + ["random"] * (k - 1), N, seed=12)
            out["strategic_v_greedy"] = sweep_players(pool, lambda k: ["strategic"] + ["greedy"] * (k - 1), N, seed=13)
        elif name == "ablate":
            out = {}
            for ab in B.ABLATED:
                out[ab] = sweep_players(pool, lambda k, ab=ab: ["strategic", ab] + ["strategic", ab][: k - 2] if k > 2 else ["strategic", ab], N, seed=21)
        elif name == "variants":
            out = {}
            V = {"no_rebound": dict(rebound=False), "win_at_end": dict(win_at_end=True), "one_contact": dict(one_contact=True),
                 "win_at_end+one_contact": dict(win_at_end=True, one_contact=True)}
            for v, kw in V.items():
                out[v] = sweep_players(pool, lambda k: ["strategic"] * k, N, kw=kw, seed=31)
        elif name == "variants_ablate":   # self-spin-only ablation under the best fix candidate
            out = {}
            kw = dict(win_at_end=True, one_contact=True)
            for ab in ("self-spin-only", "deck-only", "no-recall"):
                out[ab] = sweep_players(pool, lambda k, ab=ab: ["strategic", ab] + ["strategic", ab][: k - 2] if k > 2 else ["strategic", ab], N, kw=kw, seed=41)
        else:
            raise SystemExit("unknown section")
    out["_seconds"] = round(time.time() - t0)
    json.dump(out, open(os.path.join(OUT, name + ".json"), "w"), indent=1)
    print(name, "done in", out["_seconds"], "s")


if __name__ == "__main__":
    sec = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    section(sec, N)
