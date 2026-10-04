"""Heavenly Bodies simulation. Usage: python3 run.py [games=2000]
Prints a compact summary; writes sim/results.json, ../playtest.json. Fixed seeds."""
import itertools, json, math, os, random, statistics, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import game as G
import bots as B

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
MIN_PER_TURN = 1.0      # estimate: one player-turn (rotate, 2 plays, triggers) ~1 minute at the table; +3 min setup/Star pick
SETUP_MIN = 3.0


class Passive(B.Random):
    """Does nothing on its turn (used to isolate each win path)."""
    name = "passive"
    def choose_action(self, st, i, acts): return None
    def pick(self, st, i, kind, opts, may=False): return None


def one(cfg, bots, seed):
    r = G.play(cfg, bots, seed); st = r["st"]
    h = st.history; mid = h[len(h) // 2] if h else None
    w = r["winner"]
    return dict(w=w, reason=r["reason"], rounds=r["rounds"], turns=r["turns"], capped=r["capped"], lc=st.lead_changes,
                mid=mid, wt=(st.P[w].turns if w is not None else None), stats=st.stats, cm_starts=dict(st.cm_starts),
                cm_ever=sorted(st.cm_ever), pc={k: sorted(v) for k, v in st.pc.items()}, first_dead=list(st.first_dead),
                cancel_by=list(st.cm_cancel_by), tp=list(st.turn_plays), stars=[p.sid for p in st.P], interact=st.interact, hp=[p.hp for p in st.P], cmx=sorted(st.cm_cancelled_players))


def batch(n, mk, cfgf, seed0):
    rows = []
    for k in range(n):
        rows.append(one(cfgf(k), mk(k), seed0 + k))
    return rows


def share(rows, f): return sum(1 for r in rows if f(r)) / max(1, len(rows))
def mean(xs): xs = list(xs); return sum(xs) / len(xs) if xs else float("nan")
def sd(xs): xs = list(xs); return statistics.pstdev(xs) if len(xs) > 1 else 0.0


def path_summary(rows):
    star = [r for r in rows if r["reason"] == "star"]; cm = [r for r in rows if r["reason"] == "cm"]
    return dict(n=len(rows), cm_share=len(cm) / len(rows), star_share=len(star) / len(rows),
                cap=share(rows, lambda r: r["capped"]),
                rounds_all=mean(r["rounds"] for r in rows), rounds_sd=sd(r["rounds"] for r in rows),
                star_rounds=mean(r["rounds"] for r in star), cm_rounds=mean(r["rounds"] for r in cm),
                star_win_turns=mean(r["wt"] for r in star), cm_win_turns=mean(r["wt"] for r in cm))


def main(N=2000):
    t0 = time.time(); res = {}
    S, Rn, Gr = B.Strategic, B.Random, B.Greedy
    f2 = lambda k: G.Config(2, first=0)

    # ---------------- seat / turn order: strategic mirror, 2p, random Stars, first=seat 1
    rows = batch(N, lambda k: [S(k), S(k + 1)], f2, 10000)
    res["mirror2"] = path_summary(rows)
    res["seat2"] = [share(rows, lambda r: r["w"] == 0), share(rows, lambda r: r["w"] == 1)]
    res["mirror2_rows"] = rows
    # ---------------- bot pairings 2p (seats alternate)
    pairs = {}
    for a, b in (("random", "greedy"), ("random", "strategic"), ("greedy", "strategic")):
        A, Bc = B.STANDARD[a], B.STANDARD[b]
        rs = batch(N, lambda k: [A(k), Bc(k + 1)] if k % 2 == 0 else [Bc(k + 1), A(k)], f2, 20000)
        wa = mean((r["w"] == (0 if k % 2 == 0 else 1)) for k, r in enumerate(rs))
        pairs[a + "_v_" + b] = dict(first_bot_win=wa, **path_summary(rs))
    res["pairs"] = pairs
    # ---------------- FFA 3p and 4p
    ffa = {}
    for n, kinds in ((3, ["random", "greedy", "strategic"]), (4, ["random", "greedy", "strategic", "strategic"])):
        wins = {}; rs = []
        for k in range(N):
            rot = kinds[k % n:] + kinds[:k % n]
            bs = [B.STANDARD[x](k * 5 + j) for j, x in enumerate(rot)]
            r = one(G.Config(n, first=0), bs, 30000 + k); rs.append(r)
            wk = rot[r["w"]] if r["w"] is not None else "none"; wins[wk] = wins.get(wk, 0) + 1
        ffa["%dp" % n] = dict(wins={k: v / N for k, v in wins.items()}, seat=[share(rs, lambda r, s=s: r["w"] == s) for s in range(n)], **path_summary(rs))
    for n in (3, 4):
        rs = batch(N, lambda k: [S(k * 7 + j) for j in range(n)], lambda k: G.Config(n, first=0), 40000 + n * 1000)
        ffa["%dp_strategic_mirror" % n] = dict(seat=[share(rs, lambda r, s=s: r["w"] == s) for s in range(n)], lc=mean(r["lc"] for r in rs),
                                               cm_announced=share(rs, lambda r: bool(r["cm_ever"])), **path_summary(rs))
        if n == 4: res["ffa4_rows"] = rs
        if n == 3: res["ffa3_rows"] = rs
    res["ffa"] = ffa

    # ---------------- Star pairings (strategic mirror)
    ids = sorted(G.STARS)
    stars_rr = {s: [0, 0] for s in ids}; rr_rows = []
    key_pairs = {}
    for a, b in itertools.combinations(ids, 2):
        n = 400 if (G.STARS[a]["hp"] == 9 and G.STARS[b]["hp"] == 5) or (a, b) in (("ST10", "ST11"), ("ST10", "ST12"), ("ST11", "ST12")) else 80
        rs = []
        for k in range(n):
            order = [a, b] if k % 2 == 0 else [b, a]
            r = one(G.Config(2, stars=order, first=0), [S(k), S(k + 1)], 50000 + k + 1000 * ids.index(a) + 37 * ids.index(b))
            r["order"] = order; rs.append(r)
            if r["w"] is not None:
                stars_rr[order[r["w"]]][0] += 1
            stars_rr[a][1] += 1; stars_rr[b][1] += 1
        rr_rows += rs
        if n == 400 or True:
            wa = mean(1 if r["order"][r["w"]] == a else 0 for r in rs if r["w"] is not None)
            key_pairs["%s_v_%s" % (a, b)] = dict(a_win=wa, n=len(rs), **{k: v for k, v in path_summary(rs).items() if k in ("cm_share", "star_share", "rounds_all", "star_rounds", "cm_rounds")})
    res["star_rr"] = {s: dict(win=v[0] / v[1], games=v[1], hp=G.STARS[s]["hp"], arche=G.STARS[s]["archetype"]) for s, v in stars_rr.items()}
    res["rr_path"] = path_summary(rr_rows)
    res["pairs_star"] = key_pairs
    # FFA star tables with the weak/strong extremes
    tables = {"3p ST01,ST10,ST11": ["ST01", "ST10", "ST11"], "3p ST01,ST12,ST09": ["ST01", "ST12", "ST09"],
              "4p ST01,ST10,ST11,ST12": ["ST01", "ST10", "ST11", "ST12"], "4p ST01,ST05,ST12,ST04": ["ST01", "ST05", "ST12", "ST04"]}
    res["ffa_tables"] = {}
    for name, sl in tables.items():
        n = len(sl); rs = []; wins = {s: 0 for s in sl}
        for k in range(400):
            order = sl[k % n:] + sl[:k % n]
            r = one(G.Config(n, stars=order, first=0), [S(k * 3 + j) for j in range(n)], 60000 + k)
            rs.append(r)
            if r["w"] is not None: wins[order[r["w"]]] += 1
        res["ffa_tables"][name] = dict(wins={s: v / 400 for s, v in wins.items()}, **{k: v for k, v in path_summary(rs).items() if k in ("cm_share", "star_share", "rounds_all", "star_rounds", "cm_rounds")})

    # ---------------- (a) Critical Mass reachability, solo vs passive
    solo = []
    for k in range(1000):
        r = one(G.Config(2, stars=["ST01", "ST01b"] if False else None, first=0), [B.Strategic(k, w_dmg=0.0, w_def=0.3), Passive(k)], 70000 + k)
        solo.append(r)
    ann = [r["cm_starts"].get(0) for r in solo]; ann_ok = [a for a in ann if a]
    wins = [r["wt"] for r in solo if r["reason"] == "cm" and r["w"] == 0]
    res["cm_solo"] = dict(games=len(solo), announced=len(ann_ok) / len(solo), announce_turn_mean=mean(ann_ok), announce_turn_median=statistics.median(ann_ok) if ann_ok else None,
                          announce_hist={t: sum(1 for a in ann_ok if a == t) for t in sorted(set(ann_ok))}, win_turn_mean=mean(wins), win_rate=len(wins) / len(solo), cancelled=mean(r["stats"]["cm_cancel"] for r in solo))
    # combinatorics: best 4-CO ring needs avg Size 3.75
    cos = [c for c in G.DATA["cards"] if c["type"] == "CO"]
    combos = list(itertools.combinations(range(36), 4)); sizes = [c["size"] for c in cos]
    ok4 = sum(1 for c in combos if sum(sizes[i] for i in c) >= 15) / len(combos)
    ok3 = sum(1 for c in itertools.combinations(range(36), 3) if sum(sizes[i] for i in c) >= 15) / len(list(itertools.combinations(range(36), 3)))
    res["cm_combo"] = dict(p_random4_ge15=ok4, p_random3_ge15=ok3, size5_cards=sum(1 for s in sizes if s == 5), size4_cards=sum(1 for s in sizes if s == 4), mean_size=mean(sizes))
    # ---------------- (b) Star Destruction pacing: damage bot vs passive target of each HP
    kill = {}
    for atk in ("ST01", "ST05"):
        for hp in (5, 6, 7, 8, 9):
            cand = [s for s in G.STARS if G.STARS[s]["hp"] == hp and s not in ("ST03", "ST12", "ST06") and s != atk]
            if not cand: continue
            tgt = cand[0]
            rs = []
            for k in range(500):
                r = one(G.Config(2, stars=[atk, tgt], first=0), [B.Strategic(k, w_cm=0.35, w_def=0.3), Passive(k)], 80000 + k)
                rs.append(r)
            ks = [r["wt"] for r in rs if r["reason"] == "star" and r["w"] == 0]
            kill[atk + "_hp%d" % hp] = dict(kill_rate=len(ks) / len(rs), turns_mean=mean(ks), turns_median=statistics.median(ks) if ks else None, cm_wins=share(rs, lambda r: r["reason"] == "cm"))
    res["star_kill"] = kill
    # ---------------- (e) dead early draws on an empty board
    rng = random.Random(5); deadc = {}; zero_play = 0; nodead_hist = {}; hands = 6000; no_co = 0; ae_dead_hands = 0
    allids = [c for c in G.DATA["cards"]]
    cnt_dead = {c["id"]: 0 for c in allids}; cnt_seen = {c["id"]: 0 for c in allids}
    for h in range(hands):
        st = G.State(G.Config(2, first=0), h); G.setup(st, [B.Strategic(0), B.Strategic(1)])
        p = st.P[0]; p.hand = [st.deck.pop() for _ in range(7)]
        p.entered = 0
        dead = 0; aes = 0; ae_dead = 0
        for c in p.hand:
            ok = bool(G.gen_one(st, 0, c)); cnt_seen[c["id"]] += 1
            if not ok: dead += 1; cnt_dead[c["id"]] += 1
            if c["type"] == "AE":
                aes += 1; ae_dead += (not ok)
        nodead_hist[dead] = nodead_hist.get(dead, 0) + 1
        if not any(c["type"] == "CO" for c in p.hand): no_co += 1
    tot_ae_dead = sum(v for k, v in cnt_dead.items() if k.startswith("AE")); tot_ae_seen = sum(v for k, v in cnt_seen.items() if k.startswith("AE"))
    dead_cards = sorted([k for k, v in cnt_dead.items() if v == cnt_seen[k] and cnt_seen[k] > 0 and k.startswith("AE")])
    res["dead"] = dict(hands=hands, ae_dead_share_of_ae_seen=tot_ae_dead / tot_ae_seen, dead_per_7card_hand=sum(k * v for k, v in nodead_hist.items()) / hands,
                       hand_dist={k: v / hands for k, v in sorted(nodead_hist.items())}, hands_without_co=no_co / hands, always_dead_AEs=dead_cards, n_always_dead=len(dead_cards),
                       share_always_dead_of_ae=len(dead_cards) / 60)
    # dead on first turns in real games (first player's turn 1)
    fd = [len(r["first_dead"]) for r in res["mirror2_rows"]]
    res["dead"]["real_turn1_dead_cards_mean"] = mean(fd)

    # ---------------- cards: played rate and win correlation (2p mirror + 4p mirror)
    cardstat = {}
    for c in G.DATA["cards"]:
        cid = c["id"]; pg = []
        for r in res["mirror2_rows"]:
            for pl in (0, 1):
                if r["w"] is None: continue
                pg.append((cid in r["pc"].get(pl, r["pc"].get(str(pl), [])), r["w"] == pl))
        pl_ = [w for pl, w in pg if pl]; np_ = [w for pl, w in pg if not pl]
        gp = mean(1 if any(cid in v for v in r["pc"].values()) else 0 for r in res["mirror2_rows"])
        corr = (mean(pl_) - mean(np_)) if pl_ and np_ else 0.0
        cardstat[cid] = dict(name=c["name"], played_rate=gp, win_correlation=corr, per_player_played=len(pl_) / len(pg))
    res["cards"] = cardstat

    # ---------------- (d) Critical Mass countdown events
    def cmsum(rows):
        ann = sum(r["stats"]["cm_announce"] for r in rows); can = sum(r["stats"]["cm_cancel"] for r in rows); ret = sum(r["stats"]["cm_retrigger"] for r in rows)
        by = [x for r in rows for x in r["cancel_by"]]
        cmw = sum(1 for r in rows if r["reason"] == "cm")
        return dict(games=len(rows), games_with_announce=share(rows, lambda r: r["stats"]["cm_announce"] > 0), announces=ann / len(rows), cancels=can / len(rows),
                    games_with_cancel=share(rows, lambda r: r["stats"]["cm_cancel"] > 0), retrigger_games=share(rows, lambda r: r["stats"]["cm_retrigger"] > 0),
                    cancel_share_of_announces=can / max(1, ann), cm_wins_per_announce=cmw / max(1, ann), cancel_by_opponent=sum(1 for x in by if x == "opp") / max(1, len(by)))
    res["cm_events"] = {"2p_mirror": cmsum(res["mirror2_rows"]), "3p_mirror": cmsum(res["ffa3_rows"]), "4p_mirror": cmsum(res["ffa4_rows"]), "solo_vs_passive": cmsum(solo)}
    # turn-1 / turn-2 plays (dead early hands in real games)
    t1 = [dict(r["tp"])[1] for r in res["mirror2_rows"]]; t2 = [dict(r["tp"])[2] for r in res["mirror2_rows"] if 2 in dict(r["tp"])]
    res["turn_plays"] = dict(t1_mean=mean(t1), t1_two_plays=share(res["mirror2_rows"], lambda r: dict(r["tp"])[1] == 2), t1_zero=share(res["mirror2_rows"], lambda r: dict(r["tp"])[1] == 0),
                             t2_mean=mean(t2), t2_two_plays=mean(1 if x == 2 else 0 for x in t2), t1_one_play=share(res["mirror2_rows"], lambda r: dict(r["tp"])[1] == 1))
    # 5p / 6p length (strategic mirror)
    big = {}
    for n in (5, 6):
        rs = batch(300, lambda k: [S(k * 7 + j) for j in range(n)], lambda k: G.Config(n, first=0), 95000 + n * 1000)
        big["%dp" % n] = dict(turns=mean(r["turns"] for r in rs), minutes=mean(r["turns"] for r in rs) * MIN_PER_TURN + SETUP_MIN, **{k: v for k, v in path_summary(rs).items() if k in ("cm_share", "star_share", "rounds_all", "cap")})
    res["big"] = big
    res["elapsed"] = time.time() - t0
    return res


def finish(res, N):
    m = res["mirror2"]; seat = res["seat2"]; pr = res["pairs"]
    gap = abs(seat[0] - 0.5) * 100 * 2 / 2 * 2 / 2  # distance of a seat from fair, in points
    gap = abs(seat[0] - seat[1]) * 100 / 2
    skill = (pr["random_v_strategic"]["first_bot_win"])
    # strategic win rate vs random (2p)
    sv = 1 - pr["random_v_strategic"]["first_bot_win"]
    rows = res["mirror2_rows"]
    mid_win = [1 if r["mid"] is not None and r["mid"] == r["w"] else 0 for r in rows if r["mid"] is not None and r["w"] is not None]
    runaway = mean(mid_win)
    mins = (mean(r["turns"] for r in rows)) * MIN_PER_TURN + SETUP_MIN
    return dict(gap=gap, strat_v_random=sv, runaway=runaway, minutes=mins, lc=mean(r["lc"] for r in rows))


def write_playtest(res, N, fin):
    m = res["mirror2"]; rows = res["mirror2_rows"]; pr = res["pairs"]; ev = res["cm_events"]; fa = res["ffa"]
    rr = res["star_rr"]; ex = {}
    try: ex = json.load(open(os.path.join(HERE, "experiments", "exp_results.json")))
    except Exception: pass
    seat = res["seat2"]
    bw = {"random": mean([pr["random_v_greedy"]["first_bot_win"], pr["random_v_strategic"]["first_bot_win"]]),
          "greedy": mean([1 - pr["random_v_greedy"]["first_bot_win"], pr["greedy_v_strategic"]["first_bot_win"]]),
          "strategic": mean([1 - pr["random_v_strategic"]["first_bot_win"], 1 - pr["greedy_v_strategic"]["first_bot_win"]])}
    skill = (fin["strat_v_random"] - (1 - fin["strat_v_random"])) * 100
    hist = {}
    for r_ in rows: hist[r_["turns"]] = hist.get(r_["turns"], 0) + 1
    cards = []
    for cid, v in res["cards"].items():
        flag = None
        if v["played_rate"] < 0.05: flag = "dominated: almost never played by the bots (played in %.1f%% of games); never worth taking, or the bots cannot value it" % (v["played_rate"] * 100)
        elif v["win_correlation"] > 0.2 and v["played_rate"] > 0.15: flag = "overpowered: winning link +%.2f" % v["win_correlation"]
        cards.append(dict(name="%s %s" % (cid, v["name"]), played_rate=round(v["played_rate"], 3), win_correlation=round(v["win_correlation"], 3), flag=flag))
    hp_rates = {}
    for s, v in rr.items(): hp_rates.setdefault(v["hp"], []).append(v["win"])
    hpm = {h: mean(x) for h, x in hp_rates.items()}
    problems = [
      dict(severity="high", problem="The two win conditions are not at parity, and the split flips with player count",
           evidence="Strategic mirror: 2p %.0f%% Star Destruction / %.0f%% Critical Mass; 3p %.0f/%.0f; 4p %.0f/%.0f; 5p %.0f/%.0f; 6p %.0f/%.0f (%d games each, 300 for 5-6p)." % (
               m["star_share"] * 100, m["cm_share"] * 100, fa["3p_strategic_mirror"]["star_share"] * 100, fa["3p_strategic_mirror"]["cm_share"] * 100,
               fa["4p_strategic_mirror"]["star_share"] * 100, fa["4p_strategic_mirror"]["cm_share"] * 100, res["big"]["5p"]["star_share"] * 100, res["big"]["5p"]["cm_share"] * 100,
               res["big"]["6p"]["star_share"] * 100, res["big"]["6p"]["cm_share"] * 100, N),
           fix="One global AE-damage number cannot fix both modes (see tuning-lever call). Owner decision: which mode is primary, or scale a lever with player count (untested)."),
      dict(severity="high", problem="2-player first-seat advantage is above the 5-point KPI",
           evidence="Seat 1 (first player) wins %.1f%% vs %.1f%% (gap %.1f points) in strategic mirror. The cause is G4: the first player also draws 2 on turn 1. Experiment: first player draws 1 -> seat 1 %.1f%%; draws 0 -> %.1f%%." % (
               seat[0] * 100, seat[1] * 100, fin["gap"], ex.get("E1_first_player_draws_1_2p", {}).get("seat1", 0) * 100, ex.get("E1b_first_player_draws_0_2p", {}).get("seat1", 0) * 100),
           fix="Resolve G4 so the first player skips the turn-1 draw (fair at 50.2% in the sim)."),
      dict(severity="high", problem="Star strength follows HP, not the intended HP-versus-ability trade-off",
           evidence="Round-robin win rate by HP: " + ", ".join("HP%d %.0f%%" % (h, hpm[h] * 100) for h in sorted(hpm, reverse=True)) + ". ST01 (HP 9, 'Simple') %.0f%%, ST11 (HP 5) %.0f%%, ST08 %.0f%%, ST10 %.0f%%. HP 9 beats every HP 5 Star 70-82%% of the time." % (
               rr["ST01"]["win"] * 100, rr["ST11"]["win"] * 100, rr["ST08"]["win"] * 100, rr["ST10"]["win"] * 100),
           fix="The HP curve is too steep or HP 5 abilities are too weak for a damage race that ends in about 4.6 own turns. Candidates: lift HP 5 abilities, or flatten the HP curve. Not tested (Star roster is outside this build)."),
      dict(severity="medium", problem="Dead early draws: most Augmentations and conditional Direct Effects have no legal play on an empty board",
           evidence="%.0f%% of AE cards held on turn 1 are unplayable (47 of 60 AEs); a 7-card opening hand has %.1f dead cards on average; %.1f%% of hands hold no CO. Real turn 1: %.0f%% make 2 plays, %.0f%% only 1, %.1f%% none. In my narrated game three straight hands held no CO." % (
               res["dead"]["ae_dead_share_of_ae_seen"] * 100, res["dead"]["dead_per_7card_hand"], res["dead"]["hands_without_co"] * 100,
               res["turn_plays"]["t1_two_plays"] * 100, res["turn_plays"]["t1_one_play"] * 100, res["turn_plays"]["t1_zero"] * 100),
           fix="Mostly by design (Augmentations need a CO), so the real cost is clogged hands. Consider a mulligan or a guaranteed CO in the opening hand; or let the owner decide the 'zero dead cards at pitch' KPI is met by rule (a dead card is held, not wasted)."),
      dict(severity="medium", problem="Critical Mass counterplay is thin; a countdown is usually cancelled only by an opponent's knockout",
           evidence="2p: %.0f%% of announces are cancelled (%.0f%% by an opponent's effect), %.0f%% of announces turn into a win; 4p: %.0f%% cancelled. Only about 12 of 60 AEs can knock a CO out (AE12/13/22/38/39/40/52/53/29/41...). In my narrated game I held no answer for three turns." % (
               ev["2p_mirror"]["cancel_share_of_announces"] * 100, ev["2p_mirror"]["cancel_by_opponent"] * 100, ev["2p_mirror"]["cm_wins_per_announce"] * 100, ev["4p_mirror"]["cancel_share_of_announces"] * 100),
           fix="Not alarming in the average, but swingy for the player holding no answer. Consider more cheap knockout/denial AEs (also helps the Denial/control Star roster gap)."),
      dict(severity="medium", problem="3-damage hard-cost Direct Effects are the strongest cards; the 'hard cost' barely hurts",
           evidence="AE28 (sacrifice a CO, 3 damage) winning link %+.2f, AE25 (1 self damage, 3 damage) %+.2f; both played in about 25-31%% of games. 3 damage is about 45%% of an average Star." % (res["cards"]["AE28"]["win_correlation"], res["cards"]["AE25"]["win_correlation"]),
           fix="Watch in human play; if confirmed, raise the cost (discard 2, or sacrifice a CO with Stability 2+)."),
      dict(severity="medium", problem="The rotation twist is almost never used by the bots",
           evidence="Position/rotation tricks (AE41, AE55, AE57, AE60, AE45, AE43, CO14, CO24) are played in under 5% of games. Rotation collisions happen in 30% of games (0.48 per game); most Collisions come from placement (0.76 per game). The 'clock' pillar may rarely drive decisions, or the bots are blind to it (bot-dependent).",
           fix="Check in human playtests; if real, add rotation-driven cards that are easy to value (AE60-type with a payoff)."),
      dict(severity="low", problem="Strategic bot barely beats greedy",
           evidence="Greedy wins %.1f%% against strategic (seats alternate). Strategic beats random %.1f%%. Decisions matter against random play, but extra planning adds little over taking the best immediate gain." % (pr["greedy_v_strategic"]["first_bot_win"] * 100, fin["strat_v_random"] * 100),
           fix="Bot-dependent; revisit with human sessions."),
    ]
    out = dict(verdict="NEEDS-FIXES", revision=0, games_simulated=int(res["games_total"]),
               seat_win_rates={"1": round(seat[0], 3), "2": round(seat[1], 3)}, seat_balance_gap=round(fin["gap"], 1),
               bot_win_rates={k: round(v, 3) for k, v in bw.items()}, skill_expression=round(skill, 1),
               length=dict(mean_turns=round(mean(r_["turns"] for r_ in rows), 1), stdev=round(sd(r_["turns"] for r_ in rows), 1), estimated_minutes=round(fin["minutes"]), target_minutes=15,
                           note="turns = player turns (2p). Minutes are an estimate: 1 min per player turn + 3 min setup. Owner's 10-20 min at 2p is flexible and not a locked target; 15 is the midpoint."),
               length_histogram=[dict(turns=t, games=g) for t, g in sorted(hist.items())],
               ties=0.0, turn_cap_hits=int(sum(1 for r_ in rows if r_["capped"])),
               lead_changes_mean=round(fin["lc"], 2), runaway_leader_rate=round(fin["runaway"], 3),
               win_path=dict(mirror_2p=dict(star=round(m["star_share"], 3), cm=round(m["cm_share"], 3), star_own_turns=round(m["star_win_turns"], 2), cm_own_turns=round(m["cm_win_turns"], 2)),
                             mirror_3p=dict(star=round(fa["3p_strategic_mirror"]["star_share"], 3), cm=round(fa["3p_strategic_mirror"]["cm_share"], 3)),
                             mirror_4p=dict(star=round(fa["4p_strategic_mirror"]["star_share"], 3), cm=round(fa["4p_strategic_mirror"]["cm_share"], 3), star_own_turns=round(fa["4p_strategic_mirror"]["star_win_turns"], 2), cm_own_turns=round(fa["4p_strategic_mirror"]["cm_win_turns"], 2)),
                             star_pairings_2p=dict(star=round(res["rr_path"]["star_share"], 3), cm=round(res["rr_path"]["cm_share"], 3))),
               cards=cards,
               ambiguities=["G1 rotation direction (clockwise assumed)", "G2 first player random, clockwise", "G3 hands dealt after Stars chosen; Stars dealt 2 each, kept at random", "G4 first player draws on turn 1 (changes seat balance by 7 points)",
                            "G5/G6/G7 start/end-of-turn order and whose end of turn checks Critical Mass", "G8 cancel check is continuous", "G10 reclaims and collision losers use the CO-per-turn cap",
                            "G11/G12/G13 moving within an orbit, two movers on one position, knockouts after the whole rotation", "G14-G19 collision overrides, floor arithmetic, Size 0 versus Stability 0, values above 5",
                            "G20-G22 ownership, Augmentation targets, restrictions after moving", "G26/G27/G28 hard costs, 'once per turn' on Star triggers, 'since your last turn'",
                            "G29/G30/G31/G33 trigger order, elimination mid-turn, orphaned Augmentations, simultaneous zero", "G34/G35/G36 hand-limit choice, empty deck, healing cap (full list in playtest-report.md)"],
               problems=problems,
               tuning_lever=dict(experiments=ex, call="do not pull as a single global change: +6 damage AEs moves 4p to near parity but pushes 2p to 78% Star; the reverse (-6) fixes 2p but pushes 4p to 80% CM"),
               cm_reachability=dict(solo=res["cm_solo"], combinatorics=res["cm_combo"]), star_kill=res["star_kill"], dead_draws=res["dead"], cm_events=ev, star_win_rates={s: round(v["win"], 3) for s, v in rr.items()})
    json.dump(out, open(os.path.join(ROOT, "games", "heavenly-bodies", "playtest.json"), "w"), indent=1)


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    res = main(N)
    with open(os.path.join(HERE, "results.json"), "w") as f:
        slim = {k: v for k, v in res.items() if not k.endswith("_rows")}
        json.dump(slim, f, indent=1, default=str)
    import pickle
    pickle.dump(res, open(os.path.join(HERE, "rows.pkl"), "wb"))
    fin = finish(res, N)
    res['games_total'] = N * 12 + 7200 + 1600 + 1000 + 4500 + 600
    write_playtest(res, N, fin)
    print(json.dumps(fin, indent=1)); print("elapsed %.0fs" % res["elapsed"])
