import math, random


def mean(x): return sum(x) / len(x) if x else 0.0
def stdev(x):
    m = mean(x); return math.sqrt(sum((v - m) ** 2 for v in x) / len(x)) if x else 0.0


def wilson(k, n, z=1.96):
    """95% interval for a win rate k/n. A number within this width of a target is not settled."""
    if n == 0: return (0.0, 1.0)
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def leaders_from_diff(diffs):
    """2 players: diffs = seat0 score minus seat1 score after each turn -> leader per turn (0, 1 or None)."""
    return [0 if d > 0 else 1 if d < 0 else None for d in diffs]


def lead_changes(leaders):
    seen = [x for x in leaders if x is not None]
    return sum(1 for a, b in zip(seen, seen[1:]) if a != b)


def run_match(play, makers, n, seed=0, rotate=True):
    """Play n games. makers[i] is a callable seed -> bot. With rotate, which maker sits in which seat rotates every game,
    so seat order cannot favour one bot. Returns raw rows; use summarize() for numbers."""
    k = len(makers); rows = []
    for i in range(n):
        order = [(j + i) % k for j in range(k)] if rotate else list(range(k))   # order[seat] = maker index
        bots = [makers[order[s]](seed + i * 7 + s) for s in range(k)]
        r = dict(play(bots, seed + i)); r["order"] = order; rows.append(r)
    return rows


def summarize(rows, players=2):
    """Standard KPIs from raw rows. A tie gives every player an equal share of the win."""
    n = len(rows); seat = [0.0] * players; maker = [0.0] * players; ties = 0; caps = 0
    turns = []; lcs = []; early = []; hist = {}
    for r in rows:
        w = r.get("winner")
        if w is None:
            ties += 1
            for s in range(players): seat[s] += 1 / players; maker[r["order"][s]] += 1 / players
        else:
            seat[w] += 1; maker[r["order"][w]] += 1
        caps += bool(r.get("capped")); turns.append(r["turns"]); hist[r["turns"]] = hist.get(r["turns"], 0) + 1
        L = r.get("leaders")
        if L:
            lcs.append(lead_changes(L))
            mid = L[len(L) // 2]
            if mid is not None and w is not None: early.append(mid == w)
    seat_rates = [round(s / n, 4) for s in seat]
    return dict(games=n, seat_win_rates=seat_rates, seat_gap=round(100 * (max(seat_rates) - 1 / players), 2),
                maker_win_rates=[round(m / n, 4) for m in maker], ties=round(ties / n, 4), turn_cap_hits=caps,
                length=dict(mean_turns=round(mean(turns), 2), stdev=round(stdev(turns), 2), min=min(turns), max=max(turns)),
                length_histogram=[dict(turns=t, games=g) for t, g in sorted(hist.items())],
                lead_changes_mean=round(mean(lcs), 2) if lcs else None,
                runaway_leader_rate=round(sum(early) / len(early), 3) if early else None)


def round_robin(play, bot_makers, n, seed=0):
    """2-seat games. bot_makers: name -> maker. Returns each bot's average win rate against every other bot, the full
    pairing table, and the spread (best minus worst). Report the spread: never judge balance from one bot (lesson L2)."""
    names = list(bot_makers); pair = {}; avg = {}
    for a in names:
        w = []
        for b in names:
            if a == b: continue
            m = summarize(run_match(play, [bot_makers[a], bot_makers[b]], n, seed + 1000), 2)["maker_win_rates"][0]
            pair[f"{a} v {b}"] = m; w.append(m)
        avg[a] = round(mean(w), 4)
    return dict(avg=avg, pairs=pair, spread_pts=round(100 * (max(avg.values()) - min(avg.values())), 1))


def ablation(play, full_maker, ablated_maker, n, seed=0, threshold_pts=5.0):
    """Ablation test (lesson L1): the bot that ignores one rule must lose to the full bot by at least threshold_pts.
    margin_pts = 100 x (full win rate - ablated win rate); significant = the 95% interval of the ablated rate excludes 50%."""
    s = summarize(run_match(play, [full_maker, ablated_maker], n, seed + 5000), 2)
    full, abl = s["maker_win_rates"]
    lo, hi = wilson(round(abl * n), n)
    margin = round(100 * (full - abl), 1)
    return dict(full=full, ablated=abl, margin_pts=margin, ci_ablated=(round(lo, 3), round(hi, 3)),
                significant=(hi < 0.5 or lo > 0.5), passes=margin >= threshold_pts)
