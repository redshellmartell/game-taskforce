"""Nine Fields headline simulation. Usage: python3 run.py [games=2000] [revision=0]
Prints a compact summary; writes sim/results.json and ../playtest.json."""
import json, os, statistics, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import game as G, bots as B
SLUG_DIR = os.path.abspath(os.path.join(HERE, ".."))
N_GAMES = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
REV = int(sys.argv[2]) if len(sys.argv) > 2 else 0
S_PER_TURN, S_PER_FLOOD, S_SETUP = 15, 20, 90      # assumed human pace (seconds)

def minutes(turns, floods): return (turns * S_PER_TURN + floods * S_PER_FLOOD + S_SETUP) / 60.0

def run(n, classes, games, base_seed, rotate=True):
    """classes: list of n bot classes. Seating rotates cyclically each game. Returns list of result dicts with 'seat_of' mapping."""
    out = []
    for k in range(games):
        rot = k % n if rotate else 0
        lineup = [classes[(i + rot) % n] for i in range(n)]
        bs = [c(base_seed + k * 7 + i) for i, c in enumerate(lineup)]
        r = G.play(n, bs, base_seed + k)
        r["lineup"] = [c.name for c in lineup]
        out.append(r)
    return out

def seat_rates(rs, n):
    w = [0] * n
    for r in rs:
        for q in range(n): w[q] += r["w"][q]
    return [x / len(rs) for x in w]

def by_bot(rs):
    wins, seats = {}, {}
    for r in rs:
        for i, nm in enumerate(r["lineup"]):
            seats[nm] = seats.get(nm, 0) + 1
            wins[nm] = wins.get(nm, 0) + r["w"][i]
    return {nm: wins.get(nm, 0) / seats[nm] for nm in seats}

def lead_stats(rs):
    lc, early, early_w = [], 0, 0
    for r in rs:
        seq = [x for x in r["leads"] if x >= 0]
        lc.append(sum(1 for a, b in zip(seq, seq[1:]) if a != b))
        if r["mid"] is not None and r["mid"] >= 0:
            early += 1; early_w += r["w"][r["mid"]]
    return statistics.mean(lc), (early_w / early if early else 0.0), early

def card_stats(rs, n):
    """Per island class (value/capacity): how often claimed, and how much more often its claimer wins than 1/n."""
    cls = {}
    for r in rs:
        for q, cl in enumerate(r["st"].tcards):
            for cid in cl:
                c = G.CARDS[cid - 1]; key = "v%d cap%d" % (c[1], c[2])
                e = cls.setdefault(key, [0, 0]); e[0] += 1; e[1] += r["w"][q]
    return {k: (v[0] / len(rs), v[1] / v[0] - 1.0 / n) for k, v in cls.items()}

def main():
    t0 = time.time(); res = {}
    for n in (2, 3, 4):
        d = {}
        mirror = run(n, [B.Strategic] * n, N_GAMES, 100000 * n)
        d["seat_strategic"] = seat_rates(mirror, n)
        d["seat_greedy"] = seat_rates(run(n, [B.Greedy] * n, N_GAMES, 200000 * n), n)
        d["seat_random"] = seat_rates(run(n, [B.Random] * n, N_GAMES, 300000 * n), n)
        turns = [r["turns"] for r in mirror]; fl = [r["floods"] for r in mirror]
        d["turns_mean"] = statistics.mean(turns); d["turns_sd"] = statistics.pstdev(turns)
        d["floods_mean"] = statistics.mean(fl); d["minutes"] = minutes(d["turns_mean"], d["floods_mean"])
        d["hist"] = {}
        for t in turns: d["hist"][t // 5 * 5] = d["hist"].get(t // 5 * 5, 0) + 1
        d["ties"] = sum(r["tie"] for r in mirror) / N_GAMES
        d["cap_hits"] = sum(r["cap"] for r in mirror); d["stall_end"] = sum(r["storms"] for r in mirror) / N_GAMES
        d["lead_changes"], d["runaway"], d["runaway_n"] = lead_stats(mirror)
        d["land_share"] = sum(r["st"].acts["land"] for r in mirror) / sum(r["st"].acts["land"] + r["st"].acts["sail"] for r in mirror)
        d["cards"] = card_stats(mirror, n)
        d["score_margin"] = statistics.mean(sorted(r["scores"])[-1] - sorted(r["scores"])[-2] for r in mirror)
        # bot skill
        if n == 2:
            d["sv_random"] = by_bot(run(2, [B.Strategic, B.Random], N_GAMES, 400000))
            d["sv_greedy"] = by_bot(run(2, [B.Strategic, B.Greedy], N_GAMES, 500000))
            d["gv_random"] = by_bot(run(2, [B.Greedy, B.Random], N_GAMES, 600000))
            d["skill"] = (d["sv_random"]["strategic"] - d["sv_random"]["random"]) * 100
        else:
            lineup = [B.Random, B.Greedy, B.Strategic] + ([B.Strategic] if n == 4 else [])
            d["mixed"] = by_bot(run(n, lineup, N_GAMES, 700000 * n))
            d["skill"] = (d["mixed"]["strategic"] - d["mixed"]["random"]) * 100
        res[n] = d
    json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1, default=str)
    for n, d in res.items():
        gap = (max(d["seat_strategic"]) - 1.0 / n) * 100 if False else max(abs(x - 1.0 / n) for x in d["seat_strategic"]) * 100
        print("%dp: seats(strat) %s gap %.1f | greedy %s | random %s" % (n, [round(x, 3) for x in d["seat_strategic"]], gap,
              [round(x, 3) for x in d["seat_greedy"]], [round(x, 3) for x in d["seat_random"]]))
        print("    turns %.1f sd %.1f floods %.1f ~%.1f min | ties %.3f stall-end %.2f cap %d | lead chg %.2f runaway %.3f (n=%d) | skill gap %.1f | land %.2f margin %.1f"
              % (d["turns_mean"], d["turns_sd"], d["floods_mean"], d["minutes"], d["ties"], d["stall_end"], d["cap_hits"], d["lead_changes"],
                 d["runaway"], d["runaway_n"], d["skill"], d["land_share"], d["score_margin"]))
        print("    skill:", {k: {a: round(b, 3) for a, b in v.items()} for k, v in d.items() if k in ("sv_random", "sv_greedy", "gv_random", "mixed")})
    print("cards (3p):", {k: (round(a, 2), round(b, 3)) for k, (a, b) in sorted(res[3]["cards"].items())})
    print("done in %.0fs" % (time.time() - t0))

    write_playtest(res)

PROBLEMS = [
 {"severity": "medium", "problem": "2-player early-leader win rate is still just above the KPI and the 2p game is at the top of the length band.",
  "evidence": "2p strategic mirror, 10,000 games: early leader (leader after flood 11) wins 66.4% (KPI <= 65), lead changes 2.79 (ok), ~60.6 turns = ~24 min (+20% vs 20 target, cap 25). 3p 55.5%, 4p 48.9%. Shortening 2p makes it worse: remove 3 cards -> 69.8% runaway, 52.7 turns; remove 6 -> 74.9%, 44.9 turns.",
  "fix": "Do not shorten 2p by removing cards. Untested options: 2p storm threshold 2 x players (more storms to the trailing player), or give the trailing player in 2p the storm direction on every 3rd calm turn. Or accept 66% as within noise of the KPI and confirm with a human 2p test."},
 {"severity": "low", "problem": "Giving the storm direction to the fewest-trophies player is NOT exploitable by sandbagging.",
  "evidence": "Exploit-probe bot that avoids trophies in the first half and prefers calm moves: wins 48.2% vs 1 strategic (2p), 33.3% vs 2 strategic (3p), 23.3% vs 3 strategic (4p, fair 25%). Storms fire only 0.97/game at 2p, 0.05 at 3p, ~0 at 4p, so the storm is rarely a lever.",
  "fix": "None needed. Note the storm is mostly a 2p rule; at 3-4p it almost never fires, so the 3-4p design does not depend on it."},
 {"severity": "low", "problem": "Late 2p game is a repeat flood engine: the same island floods many times by shuffling the same pawns (Sail land share only 33% of actions at 2p).",
  "evidence": "Sample 2p log: cards 23 and 29 each flood 5+ times in turns 13-33; about half of floods are Sail-triggered. Not unbalanced, but may read as pawn shuffling rather than area control.",
  "fix": "Watch in human play. If it feels samey: a full island that has just flooded cannot be Sailed onto next turn (untested)."},
 {"severity": "low", "problem": "Score ties are common at 3-4 players and resolved by tiebreaks; some shared wins remain.",
  "evidence": "Score ties before tiebreaks: 5.9% (2p), 12.7% (3p), 19.2% (4p). Shared wins after all tiebreaks about 1.2-2.5% of games. Seat gap not affected.",
  "fix": "Acceptable. Optional: state that a shared win is possible."},
 {"severity": "low", "problem": "Small islands are weakest, value-4 strongest; nothing is dead.",
  "evidence": "3p: claimer of a v1 cap2 island wins 3.3 points less than fair; v4 cap4 claimer 11.6 more; every class is claimed 1.7-6.4 times per game.",
  "fix": "None."}]

AMBIG = G.AMBIGUITIES[:]

def write_playtest(res):
    d3, d2, d4 = res[3], res[2], res[4]
    cards = []
    for k, (rate, corr) in sorted(d3["cards"].items()):
        cards.append({"name": "island " + k, "played_rate": round(rate / 19.0, 3), "win_correlation": round(corr, 3), "flag": None})
    gap = lambda d, n: round(max(abs(x - 1.0 / n) for x in d["seat_strategic"]) * 100, 1)
    pt = {"verdict": "NEEDS-FIXES", "revision": REV, "games_simulated": N_GAMES * 14 + 10000 + 6000 + 8000 + 2000 + 8000,
          "main_player_count": 3, "note": "brief gives 2-4 players with no single main count; headline numbers are 3p, per-count numbers in by_player_count",
          "seat_win_rates": {str(i + 1): round(x, 3) for i, x in enumerate(d3["seat_strategic"])}, "seat_balance_gap": gap(d3, 3),
          "bot_win_rates": {k: round(v, 3) for k, v in d3["mixed"].items()}, "skill_expression": round(d3["skill"], 1),
          "length": {"mean_turns": round(d3["turns_mean"], 1), "stdev": round(d3["turns_sd"], 1), "estimated_minutes": round(d3["minutes"]), "target_minutes": 20},
          "length_histogram": [{"turns": k, "games": v} for k, v in sorted(d3["hist"].items())],
          "ties": round(d3["ties"], 3), "turn_cap_hits": d3["cap_hits"],
          "lead_changes_mean": round(d3["lead_changes"], 2), "runaway_leader_rate": round(d3["runaway"], 3),
          "by_player_count": {str(n): {"seat_win_rates": [round(x, 3) for x in d["seat_strategic"]], "seat_balance_gap": gap(d, n),
                              "skill_expression": round(d["skill"], 1), "mean_turns": round(d["turns_mean"], 1), "stdev": round(d["turns_sd"], 1),
                              "estimated_minutes": round(d["minutes"], 1), "ties_on_score": round(d["ties"], 3), "storms_per_game": round(d["stall_end"], 3),
                              "floods_mean": round(d["floods_mean"], 1), "lead_changes": round(d["lead_changes"], 2), "runaway_leader_rate": round(d["runaway"], 3)}
                              for n, d in res.items()},
          "cards": cards, "ambiguities": AMBIG, "problems": PROBLEMS}
    json.dump(pt, open(os.path.join(SLUG_DIR, "playtest.json"), "w"), indent=2)

if __name__ == "__main__":
    main()
