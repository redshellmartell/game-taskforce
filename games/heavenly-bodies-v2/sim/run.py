"""Heavenly Bodies v2 playtest runner (cycle 1). Usage: python3 run.py <section> [N]
Sections: headline skill ablate switches fallbacks arms newtest.  Results go to results/<section>.json (resumable by cell).
Uses simkit.run_match_parallel. Compact output only."""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools", "sim-kit"))
import simkit
from game import play
import bots as B

OUT = os.path.join(HERE, "results"); os.makedirs(OUT, exist_ok=True)
TARGET_MINUTES = 12; MPT = 0.4


def maker(spec):
    for d in (B.MAKERS, B.ABLATED, B.PERSONA):
        if spec in d: return d[spec]
    raise KeyError(spec)


def post(res, order):
    S = res["stats"]; st = res["st"]
    return dict(winner=res["winner"], turns=res["turns"], capped=res["capped"], leaders=res["leaders"], pattern=res["pattern"],
                long_night=res["long_night"], stats=S, final=[sorted(c[1] for c in o if c) for o in st.orbits],
                deck_left=len(st.deck), hand_sizes=[len(h) for h in st.hands])


def cell(specs, N, kw=None, seed=0):
    kw = kw or {}; k = len(specs)
    pl = lambda bots, sd: play(bots, sd, k, **kw)
    rows = simkit.run_match_parallel(pl, [maker(s) for s in specs], N, seed=seed, post=post)
    return digest(rows, k)


def digest(rows, players):
    s = simkit.summarize(rows, players); N = len(rows)
    tot = lambda key: sum(r["stats"][key] for r in rows)
    split = {"mass": 0.0, "const": 0.0, "align": 0.0}; combos = {}
    for r in rows:
        if r["long_night"] or r["winner"] is None: continue
        for x in r["pattern"]: split[x] += 1 / len(r["pattern"])
        key = "+".join(r["pattern"]); combos[key] = combos.get(key, 0) + 1
    pw = sum(split.values()) or 1
    spins = tot("spins") or 1; armed = tot("armed") or 1
    wins = [r for r in rows if not r["long_night"] and r["winner"] is not None]
    sizes_w = {z: 0.0 for z in range(1, 6)}
    for r in wins:
        for z in r["final"][r["winner"]]: sizes_w[z] += 1 / max(1, len(wins))
    return dict(summary=s, n=N, long_night_rate=round(sum(r["long_night"] for r in rows) / N, 4),
                pattern_share={k: round(v / pw, 3) for k, v in split.items()}, pattern_combos=combos,
                captures_per_game=round(tot("captures") / N, 2), ties_per_game=round(tot("ties") / N, 2),
                cap_by_size=[round(sum(r["stats"]["cap_by_size"][z] for r in rows) / N, 2) for z in range(1, 6)],
                crash_spin_share=round(tot("crash_spins") / spins, 3), other_spin_share=round(tot("other_spins") / spins, 3),
                formed_per_game=round(tot("formed") / N, 2), formed_survival=round(tot("formed_survived") / max(1, tot("formed")), 3),
                armed_per_game=round(tot("armed") / N, 2), armed_attacked=round(tot("armed_attacked") / armed, 3),
                armed_survived=round(tot("armed_survived") / armed, 3),
                armed_survived_if_attacked=round(tot("armed_att_survived") / max(1, tot("armed_attacked")), 3),
                recall_per_game=round(tot("recalls") / N, 2), rebound_per_game=round(tot("rebounds") / N, 2),
                winner_orbit_size_mean=[round(sizes_w[z], 2) for z in range(1, 6)],
                mean_turns=s["length"]["mean_turns"], minutes=round(s["length"]["mean_turns"] * MPT, 1))


def margin(c):
    r = c["summary"]["maker_win_rates"]; n = len(r)
    f = [r[i] for i in range(0, n, 2)]; a = [r[i] for i in range(1, n, 2)]
    return round(100 * (sum(f) / len(f) - sum(a) / len(a)), 1)


def mixed(first, other, k):    # [first, other, first, other] for ablations; first vs the rest otherwise
    return [first, other] if k == 2 else ([first, other, first] if k == 3 else [first, other, first, other])


def run_cells(name, cells, N):
    path = os.path.join(OUT, name + ".json")
    res = json.load(open(path)) if os.path.exists(path) else {}
    for key, (specs, kw, seed) in cells.items():
        if key in res: continue
        t0 = time.time(); res[key] = cell(specs, N, kw, seed); res[key]["secs"] = round(time.time() - t0)
        json.dump(res, open(path, "w"), indent=1)
        print(name, key, "done", res[key]["secs"], "s", flush=True)


SWITCH_OFF = {"win_at_start": dict(win_at_end=False), "rebound_on": dict(rebound=True), "shield_off": dict(shield=False),
              "cm15_everywhere": dict(cm_by_count=False), "rainbow_off": dict(rainbow=False), "deepspace_draw_on": dict(deepspace_draw=True)}


def sections(name, N):
    c = {}
    if name == "headline":
        for k in (2, 3, 4): c[f"{k}p"] = (["strategic"] * k, {}, 10 * k)
    elif name == "skill":
        for k in (2, 3, 4):
            c[f"strat_v_random_{k}p"] = (["strategic"] + ["random"] * (k - 1), {}, 100 + k)
            c[f"greedy_v_random_{k}p"] = (["greedy"] + ["random"] * (k - 1), {}, 200 + k)
            c[f"strat_v_greedy_{k}p"] = (["strategic"] + ["greedy"] * (k - 1), {}, 300 + k)
    elif name == "ablate":
        for ab in ("self-spin-only", "shield-blind", "threat-blind", "defence-check", "no-recall", "comet-blind"):
            for k in (2, 3, 4): c[f"{ab}_{k}p"] = (mixed("strategic", ab, k), {}, 400 + k)
    elif name == "switches":
        for sw, kw in SWITCH_OFF.items():
            for k in (2, 3, 4): c[f"{sw}_{k}p"] = (["strategic"] * k, kw, 10 * k)
    elif name == "fallbacks":
        c["2p_mass17"] = (["strategic"] * 2, dict(mass=17), 20)
        c["2p_open1"] = (["strategic"] * 2, dict(opening_2p=1), 20)
        c["2p_mass17_open1"] = (["strategic"] * 2, dict(mass=17, opening_2p=1), 20)
    elif name == "arms":
        for arm, kw in {"deck40": dict(deck40=True), "capture_to_ds": dict(capture_to_ds=True)}.items():
            for k in (2, 3, 4): c[f"{arm}_{k}p"] = (["strategic"] * k, kw, 10 * k)
    elif name == "newtest":    # NEW test: no opening bodies at any count (orbit starts empty), everything else as designed
        for k in (2, 3, 4): c[f"open0_{k}p"] = (["strategic"] * k, dict(opening=0), 10 * k)
        for k in (2, 3, 4): c[f"open1_{k}p"] = (["strategic"] * k, dict(opening=1), 10 * k)
    else: raise SystemExit("unknown section")
    return c


if __name__ == "__main__":
    sec = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    t0 = time.time(); run_cells(sec, sections(sec, N), N); print(sec, "total", round(time.time() - t0), "s")
