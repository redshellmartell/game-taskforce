"""Ladder Pairs headline run. Usage: python3 run.py [N=2000] [--json ../playtest.json]
Writes sim/results.json (all numbers) and, with --json, playtest.json (verdict taken from sim/verdict.json if present)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools", "sim-kit")); sys.path.insert(0, HERE)
import simkit
import game as Gm
from game import play, Cfg
import bots as B

TARGET_MINUTES = 25
SEC_DECISION = 6; SEC_QUICK = 2; HAND_OVERHEAD_MIN = 0.5   # ASSUMPTIONS (central): a real decision 6 s, a forced/obvious pass or play 2 s, deal+reveal+score 0.5 min per hand. Slow table (8 s / 3 s / 0.7 min) gives about 37 min.


def plays_with(cfg):
    return lambda bots, seed: play(bots, seed, cfg)


def hands_of(rows):
    return [h for r in rows for h in r["hands"]]


def pct(x): return round(100 * x, 1)


def per_bot(rows, makers_n):
    s = simkit.summarize(rows, 4)
    return s


def match(makers, n, seed, cfg=None):
    rows = simkit.run_match(plays_with(cfg) if cfg else play, makers, n, seed)
    s = simkit.summarize(rows, 4)
    s["ties"] = round(sum(r["shared"] for r in rows) / len(rows), 4)   # shared wins after all tie-breaks
    return rows, s


def hand_stats(rows):
    H = hands_of(rows); n = len(H)
    out = dict(hands=n)
    out["lead_team_3"] = round(sum(h["lead_team_3"] for h in H) / n, 3)
    out["lead_team_3_by_pairing"] = {k: round(sum(h["lead_team_3"] for h in H if h["lead_partner_pos"] == pos) / max(1, sum(1 for h in H if h["lead_partner_pos"] == pos)), 3)
                                     for k, pos in (("left_adjacent", 1), ("across", 2), ("right_adjacent", 3))}
    out["sweep_rate"] = round(sum(h["sweep"] for h in H) / n, 3)
    rt = sorted(h["rope_trick"] for h in H if h["rope_trick"] is not None)
    out["no_rope_played_rate"] = round(1 - len(rt) / n, 3)
    if rt:
        out["first_rope_trick_median"] = rt[len(rt) // 2]; out["first_rope_trick_q1_q3"] = [rt[len(rt) // 4], rt[3 * len(rt) // 4]]
    out["mean_ropes_played_per_hand"] = round(sum(h["ropes"] for h in H) / n, 2)
    out["relays_per_hand"] = round(sum(h["relays"] for h in H) / n, 3)
    fo = sum(h["forced"] for h in H); fl = sum(h["follow"] for h in H)
    out["forced_pass_rate"] = round(fo / fl, 3); out["forced_runs3_per_hand"] = round(sum(h["runs3"] for h in H) / n, 3)
    out["turns_per_hand"] = round(sum(h["turns"] for h in H) / n, 1)
    dec = sum(sum(h["decisions"]) for h in H) / n
    out["decisions_per_hand"] = round(dec, 1)
    out["minutes_per_hand"] = round((dec * SEC_DECISION + (out["turns_per_hand"] - dec) * SEC_QUICK) / 60 + HAND_OVERHEAD_MIN, 2)
    # uphill effect
    up = [(p, h["pts"][q]) for h in H for q, p in enumerate(h["uphill"])]
    u = [x for p, x in up if p]; nu = [x for p, x in up if not p]
    out["uphill_share_of_player_hands"] = round(len(u) / len(up), 3)
    out["pts_uphill_vs_not"] = [round(sum(u) / max(1, len(u)), 2), round(sum(nu) / max(1, len(nu)), 2)]
    out["no_uphill_player_hand_rate"] = round(sum(1 for h in H if not any(h["uphill"])) / n, 3)
    # card (play-type) usage: per player-hand, correlation with the player's points that hand
    cards = []
    for k, name in (("Rope", "Rope (14/15)"), ("R", "Run lead/follow"), ("T", "Triple"), ("P", "Pair"), ("S", "Single (number)")):
        xs = [(1 if k in h["kinds"][q] else 0, h["pts"][q] / (2 if h["uphill"][q] else 1)) for h in H for q in range(4)]
        m = sum(x for x, _ in xs) / len(xs); my = sum(y for _, y in xs) / len(xs)
        cov = sum((x - m) * (y - my) for x, y in xs); vx = sum((x - m) ** 2 for x, _ in xs); vy = sum((y - my) ** 2 for _, y in xs)
        corr = cov / (vx * vy) ** 0.5 if vx and vy else 0.0
        cards.append(dict(name=k and name, played_rate=round(m, 3), win_correlation=round(corr, 3), flag=("rarely played" if m < 0.05 else None)))
    out["cards"] = cards
    return out


def game_stats(rows):
    n = len(rows)
    a3 = [r for r in rows if len(r["leaders"]) > 2 and r["leaders"][2] is not None]
    out = dict(runaway_after_hand3=round(sum(r["leaders"][2] == r["winner"] for r in a3) / max(1, len(a3)), 3))
    # was a player ever Uphill and did a once-Uphill player win?
    ever = sum(1 for r in rows if any(any(h["uphill"][r["winner"]] for h in [hh]) for hh in r["hands"]))
    out["winner_was_uphill_at_some_hand"] = round(ever / n, 3)
    out["winner_uphill_in_hand_2_to_5_rate"] = round(sum(1 for r in rows if any(r["hands"][i]["uphill"][r["winner"]] for i in range(1, 5))) / n, 3)
    return out


def pair_table(makers, names, n, seed):
    """makers listed in seat-rotation order; returns per-name average win rate per bot (mean of that name's makers)."""
    rows, s = match(makers, n, seed)
    byname = {}
    for nm, w in zip(names, s["maker_win_rates"]): byname.setdefault(nm, []).append(w)
    return {nm: round(sum(v) / len(v), 4) for nm, v in byname.items()}, s, rows


def main(n=2000, json_path=None):
    R = {}
    R_, G_, X_ = B.Reader, B.Greedy, B.Random
    # 1. headline: Reader mirror and Greedy mirror (L2: two bots of different strength)
    rows, summ = match([R_] * 4, n, 100); R["mirror_reader"] = dict(summary={k: v for k, v in summ.items() if k != "length_histogram"}, **hand_stats(rows), **game_stats(rows))
    rowsg, summg = match([G_] * 4, n, 200); R["mirror_greedy"] = dict(summary={k: v for k, v in summg.items() if k != "length_histogram"}, **hand_stats(rowsg), **game_stats(rowsg))
    # 2. skill / spread
    t = {}
    t["1R_v_3Random"] = pair_table([R_, X_, X_, X_], ["reader", "random", "random", "random"], n, 300)[0]
    t["1R_v_3Greedy"] = pair_table([R_, G_, G_, G_], ["reader", "greedy", "greedy", "greedy"], n, 400)[0]
    t["1G_v_3Random"] = pair_table([G_, X_, X_, X_], ["greedy", "random", "random", "random"], n, 500)[0]
    t["2R_v_2Random"] = pair_table([R_, R_, X_, X_], ["reader", "reader", "random", "random"], n, 600)[0]
    t["2R_v_2Greedy"] = pair_table([R_, R_, G_, G_], ["reader", "reader", "greedy", "greedy"], n, 700)[0]
    t["2G_v_2Random"] = pair_table([G_, G_, X_, X_], ["greedy", "greedy", "random", "random"], n, 800)[0]
    RB = B.ReaderBest
    t["1RB_v_3Random"] = pair_table([RB, X_, X_, X_], ["reader", "random", "random", "random"], n, 310)[0]
    t["2RB_v_2Greedy"] = pair_table([RB, RB, G_, G_], ["reader", "reader", "greedy", "greedy"], n, 710)[0]
    t["2RB_v_2Reader"] = pair_table([RB, RB, R_, R_], ["reader", "reader", "abl", "abl"], n, 720)[0]
    R["tables"] = t
    gaps = {"reader_minus_random_1v3": pct(t["1R_v_3Random"]["reader"] - t["1R_v_3Random"]["random"]),
            "reader_minus_random_2v2": pct(t["2R_v_2Random"]["reader"] - t["2R_v_2Random"]["random"]),
            "reader_minus_greedy_1v3": pct(t["1R_v_3Greedy"]["reader"] - t["1R_v_3Greedy"]["greedy"]),
            "reader_minus_greedy_2v2": pct(t["2R_v_2Greedy"]["reader"] - t["2R_v_2Greedy"]["greedy"]),
            "readerbest_minus_random_1v3": pct(t["1RB_v_3Random"]["reader"] - t["1RB_v_3Random"]["random"]),
            "readerbest_minus_greedy_2v2": pct(t["2RB_v_2Greedy"]["reader"] - t["2RB_v_2Greedy"]["greedy"]),
            "greedy_minus_random_1v3": pct(t["1G_v_3Random"]["greedy"] - t["1G_v_3Random"]["random"])}
    R["skill_gaps_pts"] = gaps
    # 3. ablations (2 Reader + 2 ablated, seats rotated); margin = per-bot win-rate difference in points (and pair-share difference)
    R["ablations"] = {}
    for k, mk in B.ABL.items():
        tt = pair_table([R_, R_, mk, mk], ["reader", "reader", "abl", "abl"], n, 1000 + len(k))[0]
        R["ablations"][k] = dict(reader=tt["reader"], ablated=tt["abl"], margin_per_bot_pts=pct(tt["reader"] - tt["abl"]), margin_pair_share_pts=pct(2 * (tt["reader"] - tt["abl"])), passes=pct(tt["reader"] - tt["abl"]) >= 5)
    tt = pair_table([B.CODE, B.CODE, R_, R_], ["code", "code", "reader", "reader"], n, 2000)[0]
    R["code_attack"] = dict(code=tt["code"], honest=tt["reader"], gain_pair_share_pts=pct(2 * tt["code"] - 0.5 * 1 - 0.0) if False else pct(2 * tt["code"] - 0.5), passes=pct(2 * tt["code"] - 0.5) <= 3)
    # 4. rule variants (Reader mirror): Uphill off, Relay off
    rows_u, s_u = match([R_] * 4, n, 100, Cfg(uphill=False))
    R["uphill_off"] = dict(runaway=s_u["runaway_leader_rate"], lead_changes=s_u["lead_changes_mean"], seat_gap=s_u["seat_gap"], **game_stats(rows_u),
                           runaway_delta_pts=pct(s_u["runaway_leader_rate"] - summ["runaway_leader_rate"]))
    rows_r, s_r = match([R_] * 4, n, 100, Cfg(relay=False))
    hr = hand_stats(rows_r)
    R["relay_off"] = dict(sweep_rate=hr["sweep_rate"], lead_team_3=hr["lead_team_3"], seat_gap=s_r["seat_gap"], lead_changes=s_r["lead_changes_mean"])
    with open(os.path.join(HERE, "results.json"), "w") as f: json.dump(R, f, indent=1)
    m = R["mirror_reader"]; ms = m["summary"]
    mins = round(ms["length"]["mean_turns"] / m["turns_per_hand"] * m["minutes_per_hand"] * 1.0, 1)
    print(f"{n} games per config. Reader mirror: seat wins {ms['seat_win_rates']} gap {ms['seat_gap']}; length {ms['length']['mean_turns']} turns ({m['turns_per_hand']}/hand) ~{mins} min (assumed {SEC_DECISION}s/decision, {SEC_QUICK}s quick turn, {HAND_OVERHEAD_MIN} min/hand overhead)")
    print(f"  Greedy mirror: seat gap {R['mirror_greedy']['summary']['seat_gap']}; runaway {R['mirror_greedy']['summary']['runaway_leader_rate']}; lead changes {R['mirror_greedy']['summary']['lead_changes_mean']}")
    print(f"  runaway (after hand 4 / hand 3): {ms['runaway_leader_rate']} / {m['runaway_after_hand3']}; lead changes {ms['lead_changes_mean']}; shared-win ties {ms['ties']}; caps {ms['turn_cap_hits']}")
    print(f"  first-lead team 3+: {m['lead_team_3']} by pairing {m['lead_team_3_by_pairing']}; greedy {R['mirror_greedy']['lead_team_3']} {R['mirror_greedy']['lead_team_3_by_pairing']}")
    print(f"  Rope first trick median {m.get('first_rope_trick_median')} IQR {m.get('first_rope_trick_q1_q3')}; no Rope in {m['no_rope_played_rate']} of hands; ropes/hand {m['mean_ropes_played_per_hand']}; relays/hand {m['relays_per_hand']}")
    print(f"  forced-pass rate {m['forced_pass_rate']}; runs of 3+ forced per hand {m['forced_runs3_per_hand']}; uphill share {m['uphill_share_of_player_hands']} pts uphill vs not {m['pts_uphill_vs_not']}")
    print("  skill gaps (pts):", gaps); print("  tables:", t)
    for k, a in R["ablations"].items(): print(f"  {'PASS' if a['passes'] else 'FAIL'} {k}: reader {a['reader']} vs abl {a['ablated']} (per-bot margin {a['margin_per_bot_pts']}, pair-share margin {a['margin_pair_share_pts']})")
    print(f"  code attack: pair share {R['code_attack']['code']*2:.3f} gain {R['code_attack']['gain_pair_share_pts']} pts ({'PASS' if R['code_attack']['passes'] else 'FAIL'})")
    print(f"  Uphill off: runaway {R['uphill_off']['runaway']} (delta {R['uphill_off']['runaway_delta_pts']} pts), lead changes {R['uphill_off']['lead_changes']}; Relay off: sweep {R['relay_off']['sweep_rate']} vs {m['sweep_rate']}")
    if json_path:
        vp = os.path.join(HERE, "verdict.json"); V = json.load(open(vp)) if os.path.exists(vp) else {}
        gap = gaps["reader_minus_random_1v3"]
        out = simkit.to_playtest_json(summ, {"random": t["1R_v_3Random"]["random"], "greedy": t["1G_v_3Random"]["greedy"], "strategic": t["1R_v_3Random"]["reader"]},
                                      gap, TARGET_MINUTES, mins, V.get("verdict", "NEEDS-FIXES"), 0, cards=m["cards"], ambiguities=Gm.AMBIGUITIES, problems=V.get("problems", []))
        out["games_simulated"] = n; out["ablations"] = R["ablations"]; out["code_attack"] = R["code_attack"]; out["skill_gaps_pts"] = gaps
        out["bot_spread_note"] = "bot averages from 1+3 tables vs Random; see sim/results.json"
        out["validation"] = "bots only, unvalidated"
        with open(json_path, "w") as f: json.dump(out, f, indent=2)
        print("wrote", json_path)


if __name__ == "__main__":
    a = sys.argv[1:]; nums = [x for x in a if x.isdigit()]
    main(int(nums[0]) if nums else 2000, a[a.index("--json") + 1] if "--json" in a else None)
