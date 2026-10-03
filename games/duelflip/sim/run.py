import sys, json, math, collections
from game import Config, play, SPECIES
import bots as B
import notes as N

def mk(spec, seed):
    """spec: name or name:leave_mode"""
    if ":" in spec:
        n, m = spec.split(":"); return B.ALL[n](seed, leave_mode=m)
    return B.ALL[spec](seed)

class Rec:
    """Wraps a bot and records whether each leave choice was simply the lowest card (no change to play)."""
    def __init__(self, bot, log): self.bot = bot; self.log = log
    def __getattr__(self, k): return getattr(self.bot, k)
    def leave(self, st, p, cands):
        i = self.bot.leave(st, p, cands)
        if len(cands) > 1:
            self.log.append((self.bot.name, st.river[i][1] == min(st.river[j][1] for j in cands)))
        return i

def winner_without_species(cfg, st):
    """Who would have won with no species bonus? (same tiebreaks as the real game)"""
    s0 = sum(v for _, v in st.haul[0]); s1 = sum(v for _, v in st.haul[1]) + cfg.second_pts
    if s0 > s1: return 0
    if s1 > s0: return 1
    return 0 if len(st.haul[0]) > len(st.haul[1]) else 1

def match(cfg, a, b, n, base=0):
    R = dict(a_wins=0, first_wins=0, ties=0, caps=0, turns=[], lc=[], el=0, eln=0, busts=0, games=0,
             small_busts=0, bait_busts=0, scout=0, flips=0, bust_pile=[], bank_pile=[], left=[], refunds=0, forced=0, scores=[],
             el_half=0, eln_half=0, species_decisive=0, maj_x=[], maj_win=[], refund_x=[], refund_win=[], leave_log=[], ties_n=0)
    for i in range(n):
        seed = base + i; a_first = (i % 2 == 0)
        bs = (mk(a, seed), mk(b, seed + 1)) if a_first else (mk(b, seed + 1), mk(a, seed))
        bs = tuple(Rec(x, R["leave_log"]) for x in bs)
        r = play(cfg, bs, seed); st = r["st"]
        a_seat = 0 if a_first else 1; w = r["winner"]
        R["a_wins"] += (w == a_seat); R["first_wins"] += (w == 0)
        R["ties"] += r["tie"]; R["caps"] += r["capped"]; R["turns"].append(r["turns"])
        h = st.history; sg = [x for x in ((d > 0) - (d < 0) for d in h) if x]
        R["lc"].append(sum(1 for x, y in zip(sg, sg[1:]) if x != y))
        k = len(h) // 3
        if k and h[k]: R["eln"] += 1; R["el"] += ((h[k] > 0) == (w == 0))
        k2 = len(h) // 2
        if k2 and h[k2]: R["eln_half"] += 1; R["el_half"] += ((h[k2] > 0) == (w == 0))
        R["species_decisive"] += (winner_without_species(cfg, st) != w)
        for pl in (0, 1):
            maj = sum(1 for sp in range(SPECIES) if sum(1 for x, _ in st.haul[pl] if x == sp) > sum(1 for x, _ in st.haul[1 - pl] if x == sp))
            R["maj_x"].append(maj); R["maj_win"].append(int(w == pl))
            R["refund_x"].append(int(st.stats["refunds"][pl] > 0)); R["refund_win"].append(int(w == pl))
        s = st.stats
        R["busts"] += s["busts"]; R["small_busts"] += s["small_busts"]; R["bait_busts"] += s["bait_clash_busts"]
        R["scout"] += s["scout_discards"]; R["flips"] += s["flips"]; R["bust_pile"] += s["bust_pile"]
        R["bank_pile"] += s["bank_pile"]; R["left"] += s["left_vals"]; R["refunds"] += sum(s["refunds"]); R["forced"] += s["forced_empty_end"]
        R["scores"].append(sum(r["scores"]))
        R["games"] += 1
    return R

def mean(x): return sum(x) / len(x) if x else 0.0

def mirror_line(nm, R, n):
    t = R["turns"]
    return ("%-22s seat1 %.1f%%  ties %.2f%%  caps %d  turns %.1f (%d-%d)  LC %.1f  earlyLeadWin %.0f%%  busts/g %.2f  bust/turn %.1f%%  1-card-busts/g %.2f  bait-busts/g %.2f  avgbustpile %.1f  avgbankpile %.1f"
            % (nm, 100 * R["first_wins"] / n, 100 * R["ties"] / n, R["caps"], mean(t), min(t), max(t), mean(R["lc"]),
               100 * R["el"] / max(1, R["eln"]), R["busts"] / n, 100 * R["busts"] / sum(t), R["small_busts"] / n, R["bait_busts"] / n,
               mean(R["bust_pile"]), mean(R["bank_pile"])))

def corr(x, y):
    """Pearson correlation (point-biserial when y is 0/1). None if either side never varies."""
    n = len(x)
    if n < 2: return None
    mx, my = sum(x) / n, sum(y) / n
    sx = math.sqrt(sum((a - mx) ** 2 for a in x)); sy = math.sqrt(sum((b - my) ** 2 for b in y))
    if sx == 0 or sy == 0: return None
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)

def write_playtest_json(path, n):
    """Re-run the v2 simulation and write playtest.json in the format the dashboard reads (see CLAUDE.md)."""
    cfg = Config(); names = list(B.ALL)
    total = 0; caps = 0; avg = {}
    for a in names:                                   # round robin: each bot's average win rate over every opponent
        wins = []
        for b in names:
            if a == b: continue
            R = match(cfg, a, b, n); total += n; caps += R["caps"]; wins.append(R["a_wins"] / n)
        avg[a] = mean(wins)
    mirrors = {}
    for nm in names:                                  # mirror matches: seat balance, length, lead changes
        mirrors[nm] = match(cfg, nm, nm, n, base=100000); total += n; caps += mirrors[nm]["caps"]
    S = mirrors["strategic"]                          # the benchmark bot for everything per-game below
    seat1 = S["first_wins"] / n
    gap = max(abs(100 * m["first_wins"] / n - 50) for m in mirrors.values())
    t = S["turns"]; mu = mean(t); sd = math.sqrt(sum((x - mu) ** 2 for x in t) / len(t))
    hist = sorted(collections.Counter(t).items())
    strat_leaves = [low for name, low in S["leave_log"] if name == "strategic"]
    mp = sum(1 for x in S["maj_x"] if x > 0) / len(S["maj_x"])
    rp = sum(S["refund_x"]) / len(S["refund_x"])
    # Design elements (not individual cards). played_rate is measured; the judgement in "flag" is the playtester's (notes.py).
    banks = len(S["bank_pile"])                       # banks that had a leave decision
    cards = [
        {"name": "Species majority bonus", "played_rate": round(mp, 3), "win_correlation": None, "flag": N.CARD_FLAGS["Species majority bonus"]},
        {"name": "Lifebuoy refund", "played_rate": round(rp, 3), "win_correlation": None, "flag": N.CARD_FLAGS["Lifebuoy refund"]},
        {"name": "Bait (leave one card)", "played_rate": round(len(strat_leaves) / max(1, banks), 3), "win_correlation": None, "flag": N.CARD_FLAGS["Bait (leave one card)"]},
    ]
    out = {
        "verdict": N.VERDICT, "revision": N.REVISION, "games_simulated": total,
        "seat_win_rates": {"1": round(seat1, 3), "2": round(1 - seat1, 3)}, "seat_balance_gap": round(gap, 1),
        "bot_win_rates": {k: round(v, 3) for k, v in avg.items()}, "skill_expression": round(100 * (avg["strategic"] - avg["random"]), 1),
        "length": {"mean_turns": round(mu, 1), "stdev": round(sd, 1), "estimated_minutes": N.ESTIMATED_MINUTES, "target_minutes": N.TARGET_MINUTES},
        "length_histogram": [{"turns": k, "games": v} for k, v in hist],
        "ties": round(S["ties"] / n, 4), "turn_cap_hits": caps,
        "lead_changes_mean": round(mean(S["lc"]), 1), "runaway_leader_rate": round(S["el_half"] / max(1, S["eln_half"]), 3),
        "cards": cards, "ambiguities": N.AMBIGUITIES, "problems": N.PROBLEMS,
    }
    with open(path, "w") as f: json.dump(out, f, indent=2); f.write("\n")
    print("wrote %s: %d games, seat 1 %.1f%% (benchmark: strategic mirror), worst seat gap %.1f pts, skill %.1f pts, halfway-leader wins %.0f%%, one-third-leader wins %.0f%%, species decides %.1f%% of games"
          % (path, total, 100 * seat1, gap, out["skill_expression"], 100 * out["runaway_leader_rate"], 100 * S["el"] / max(1, S["eln"]), 100 * S["species_decisive"] / n))
    return out

if __name__ == "__main__":
    if "--json" in sys.argv:                          # python3 run.py 2000 --json ../playtest.json
        i = sys.argv.index("--json"); path = sys.argv[i + 1]
        nums = [a for a in sys.argv[1:i] if a.isdigit()]
        write_playtest_json(path, int(nums[0]) if nums else 2000)
        sys.exit(0)
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    cfg = Config()
    names = list(B.ALL)
    print("== Round robin, win%% of ROW vs COL, n=%d/pair, seats alternate" % n)
    print("%-14s" % "" + "".join("%-14s" % c[:13] for c in names) + "avg")
    for a in names:
        row = []
        for b in names:
            row.append(None if a == b else 100 * match(cfg, a, b, n)["a_wins"] / n)
        v = [x for x in row if x is not None]
        print("%-14s" % a + "".join("%-14s" % ("-" if x is None else "%.1f" % x) for x in row) + "%.1f" % mean(v))
    print("\n== Mirror matches")
    for nm in names:
        print(mirror_line(nm, match(cfg, nm, nm, n, base=100000), n))
