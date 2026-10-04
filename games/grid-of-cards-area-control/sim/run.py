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
    for r in rs: w[r["winner"]] += 1
    return [x / len(rs) for x in w]

def by_bot(rs):
    wins, seats = {}, {}
    for r in rs:
        for i, nm in enumerate(r["lineup"]):
            seats[nm] = seats.get(nm, 0) + 1
            if r["winner"] == i: wins[nm] = wins.get(nm, 0) + 1
    return {nm: wins.get(nm, 0) / seats[nm] for nm in seats}

def lead_stats(rs):
    lc, early, early_w = [], 0, 0
    for r in rs:
        seq = [x for x in r["leads"] if x >= 0]
        lc.append(sum(1 for a, b in zip(seq, seq[1:]) if a != b))
        if r["mid"] is not None and r["mid"] >= 0:
            early += 1; early_w += (r["mid"] == r["winner"])
    return statistics.mean(lc), (early_w / early if early else 0.0), early

def card_stats(rs, n):
    """Per island class (value/capacity): how often claimed, and how much more often its claimer wins than 1/n."""
    cls = {}
    for r in rs:
        for q, cl in enumerate(r["st"].tcards):
            for cid in cl:
                c = G.CARDS[cid - 1]; key = "v%d cap%d" % (c[1], c[2])
                e = cls.setdefault(key, [0, 0]); e[0] += 1; e[1] += (r["winner"] == q)
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
        d["cap_hits"] = sum(r["cap"] for r in mirror); d["stall_end"] = sum(r["stall"] for r in mirror) / N_GAMES
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
 {"severity": "high", "problem": "At 2 players the game mostly ends on the stall limit, not on the deck: only ~14.5 of 22 floods happen, a third of the deck is never used, and length is erratic.",
  "evidence": "2p strategic mirror: stall-end 58% of games (73-88% when an exploit-probe or expert bot plays), turns 41.8 sd 17.6, lead changes 1.77 (KPI >= 2), early-leader wins 68.7% (KPI <= 65%). 3p: stall-end 5%, 4p: 0%.",
  "fix": "Do not let the stall limit end the game. Untested: when 3 x players turns pass with no flood, a 'storm' floods the fullest island (next player picks direction), so every game runs the full deck. A longer stall limit alone does not fix it (6 x players still ends 37% of 2p games and runaway stays 69%)."},
 {"severity": "medium", "problem": "Many games are decided on a tiebreak, and the tiebreaks lean to later seats.",
  "evidence": "Score ties before tiebreaks: 7.5% (2p), 11.4% (3p), 17.4% (4p). Average margin of victory only 4.5 / 3.0 / 2.2 pearls. Seat win rates still within 3.2 points of fair.",
  "fix": "Acceptable for the KPI, but consider a more neutral last tiebreak (for example most islands, then fewest pawns left on the board) so late seats do not collect close finishes."},
 {"severity": "medium", "problem": "Simulated length is above target at 3-4 players and the estimate rests on an assumed pace.",
  "evidence": "~22.2 min (3p) and ~22.6 min (4p) vs 20 target (+11% / +13%, inside the 20% band, near the 25 min cap); 2p ~16.8 min. Pace assumed 15 s per turn + 20 s per flood + 90 s setup.",
  "fix": "If a human playtest runs long, deal 18 islands instead of 21 (fewer floods) or drop the 3x players stall limit to 2x."},
 {"severity": "low", "problem": "Deeper search helps in 2 players but barely in 3 players against a greedy bot.",
  "evidence": "Experiment: 2-ply bot beats 1-ply strategic 67.7% at 2p, but in 3p the 2-ply bot wins 41.3% vs greedy 40.3% (1-ply 18.4%). Could be a bot limit (it only models the next player) or real kingmaking noise.",
  "fix": "Check with humans at 3p. If it holds, the trigger's direction choice at 3-4p is too swingy to plan around."},
 {"severity": "low", "problem": "Value-1 two-capacity islands are the weakest class; value-4 islands are the strongest.",
  "evidence": "Claimer of a v1 cap2 island wins 4.5 points less often than fair (3p); claimer of a v4 island wins 13.4 points more. Nothing is dead.",
  "fix": "None needed; keep an eye on it."}]

AMBIG = G.AMBIGUITIES[:]

def write_playtest(res):
    d3, d2, d4 = res[3], res[2], res[4]
    cards = []
    for k, (rate, corr) in sorted(d3["cards"].items()):
        cards.append({"name": "island " + k, "played_rate": round(rate / 21.4, 3), "win_correlation": round(corr, 3), "flag": None})
    gap = lambda d, n: round(max(abs(x - 1.0 / n) for x in d["seat_strategic"]) * 100, 1)
    pt = {"verdict": "NEEDS-FIXES", "revision": REV, "games_simulated": N_GAMES * 3 * 3 + N_GAMES * 3 * 3,
          "main_player_count": 3, "note": "brief gives 2-4 players with no single main count; headline numbers are 3p, per-count numbers in by_player_count",
          "seat_win_rates": {str(i + 1): round(x, 3) for i, x in enumerate(d3["seat_strategic"])}, "seat_balance_gap": gap(d3, 3),
          "bot_win_rates": {k: round(v, 3) for k, v in d3["mixed"].items()}, "skill_expression": round(d3["skill"], 1),
          "length": {"mean_turns": round(d3["turns_mean"], 1), "stdev": round(d3["turns_sd"], 1), "estimated_minutes": round(d3["minutes"]), "target_minutes": 20},
          "length_histogram": [{"turns": k, "games": v} for k, v in sorted(d3["hist"].items())],
          "ties": round(d3["ties"], 3), "turn_cap_hits": d3["cap_hits"],
          "lead_changes_mean": round(d3["lead_changes"], 2), "runaway_leader_rate": round(d3["runaway"], 3),
          "by_player_count": {str(n): {"seat_win_rates": [round(x, 3) for x in d["seat_strategic"]], "seat_balance_gap": gap(d, n),
                              "skill_expression": round(d["skill"], 1), "mean_turns": round(d["turns_mean"], 1), "stdev": round(d["turns_sd"], 1),
                              "estimated_minutes": round(d["minutes"], 1), "ties_on_score": round(d["ties"], 3), "stall_limit_end_rate": round(d["stall_end"], 3),
                              "floods_mean": round(d["floods_mean"], 1), "lead_changes": round(d["lead_changes"], 2), "runaway_leader_rate": round(d["runaway"], 3)}
                              for n, d in res.items()},
          "cards": cards, "ambiguities": AMBIG, "problems": PROBLEMS}
    json.dump(pt, open(os.path.join(SLUG_DIR, "playtest.json"), "w"), indent=2)

if __name__ == "__main__":
    main()
