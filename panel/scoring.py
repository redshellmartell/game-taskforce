#!/usr/bin/env python3
"""Free fun-profile scoring for the test panel (standard library only).

Reads, for one game:
  games/<slug>/playtest.json            game-level numbers from the playtester
  games/<slug>/rules.md                 (word count -> rules_simplicity)
  games/<slug>/sim/panel-results.json   persona-bot rotation results (written by the game's sim/panel_run.py)
  panel/personas/*.md                   weights, preferred minutes, price tolerance, pet peeves
and writes games/<slug>/panel.json (stage "scores"; the AI reviews fill in "review" later).

Every metric is normalised to 0-1 (1 = best for the player). A persona's predicted fun is
    fun = 1 + 4 * sum(weight_i * metric_i)          (weights come from the persona file and sum to 1)

Usage:  python3 panel/scoring.py <slug> [--revision N]
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

METRICS = ["skill_expression", "decisions_per_turn", "lead_changes", "length_fit",
           "rules_simplicity", "catch_up", "interaction", "dominant_strategy_absent", "originality"]


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


# ---------------------------------------------------------------- persona files
def _scalar(v):
    v = v.split("#")[0].strip() if not v.strip().startswith(('"', "'")) else v.strip()
    if v.startswith("[") and v.endswith("]"):
        return [_scalar(x) for x in v[1:-1].split(",") if x.strip()]
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return v


def parse_frontmatter(text):
    """Tiny parser for the persona files: scalars, one-line lists and one level of nested keys."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    out, cur = {}, None
    if not m:
        return out
    for line in m.group(1).split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indented = line.startswith((" ", "\t"))
        key, _, val = line.strip().partition(":")
        if indented and cur is not None:
            out[cur][key] = _scalar(val)
        elif val.split("#")[0].strip() == "":
            out[key] = {}
            cur = key
        else:
            out[key] = _scalar(val)
            cur = None
    return out


def pet_peeve_titles(text):
    sec = re.search(r"^## Pet peeves\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not sec:
        return []
    return [re.sub(r"\*\*", "", m.group(1)).strip()
            for m in re.finditer(r"^\d+\.\s+(.*)$", sec.group(1), re.M)]


def load_personas(root=ROOT, only=None):
    d = os.path.join(root, "panel", "personas")
    out = {}
    for f in sorted(os.listdir(d)):
        if not f.endswith(".md"):
            continue
        text = open(os.path.join(d, f), encoding="utf-8").read()
        fm = parse_frontmatter(text)
        if not fm.get("id") or (only and fm["id"] not in only):
            continue
        fm["peeves"] = pet_peeve_titles(text)
        out[fm["id"]] = fm
    return out


# ---------------------------------------------------------------- metrics
def rules_simplicity(words):
    """600 words or fewer = 1, 3000 or more = 0, linear between."""
    return clamp(1 - (words - 600) / 2400)


def length_fit(minutes, preferred):
    """1 inside the persona's preferred range, falling to 0 as the game gets as far outside it as the range's own start."""
    lo, hi = preferred
    if lo <= minutes <= hi:
        return 1.0
    if minutes < lo:
        return clamp(1 - (lo - minutes) / lo)
    return clamp(1 - (minutes - hi) / hi)


def skill_expression(points):
    """Strategic-vs-random win-rate gap in points (KPI target is 20). 40 points or more = 1."""
    return clamp(points / 40.0)


def dominant_absent(cards):
    """Share of the game's design elements the playtester did not flag as 'dominated'."""
    if not cards:
        return 1.0
    dominated = sum(1 for c in cards if "dominated" in (c.get("flag") or "").lower())
    return clamp(1 - dominated / len(cards))


def originality(brief):
    """The researcher's originality score for the idea (1-5 in brief.json's rubric) as 0-1; None if the brief has none."""
    v = ((brief or {}).get("rubric") or {}).get("originality")
    return clamp((v - 1) / 4.0) if isinstance(v, (int, float)) else None


def game_metrics(playtest, rules_words, preferred, brief=None):
    """Metrics that depend on the game and the persona's taste, not on how the persona's bot played."""
    minutes = (playtest.get("length") or {}).get("estimated_minutes") or 0
    extra = {"originality": originality(brief)}
    return {**{k: v for k, v in extra.items() if v is not None},
        "skill_expression": skill_expression(playtest.get("skill_expression") or 0),
        "length_fit": length_fit(minutes, preferred),
        "rules_simplicity": rules_simplicity(rules_words),
        "dominant_strategy_absent": dominant_absent(playtest.get("cards") or []),
    }


def bot_metrics(r):
    """Metrics measured from a persona bot's games. `r` holds raw rotation numbers (see sim/panel_run.py)."""
    return {
        "decisions_per_turn": clamp(r["decisions_per_turn"] / 3.0),      # 3+ real decisions a turn = 1
        "lead_changes": clamp(r["lead_changes"] / 4.0),                  # 4+ lead changes a game = 1 (KPI floor is 2 = 0.5)
        "catch_up": clamp(r["comeback_rate"] / 0.5),                     # winning half of the games you trailed in = 1
        "interaction": clamp(r["interaction_rate"] / 0.3),               # 30% of turns changing hands = 1
    }


def weighted(metrics, weights):
    """Weighted mean of the metrics. A metric that is not available (for example originality when the game has no
    brief.json) is left out and the remaining weights are scaled up, so a missing number never counts as zero."""
    have = {k: w for k, w in weights.items() if k in metrics and w > 0}
    total = sum(have.values())
    return sum(w * metrics[k] for k, w in have.items()) / total if total else 0.0


def fun_from_metrics(metrics, weights):
    return round(1 + 4 * weighted(metrics, weights), 2)


def replay_from_metrics(metrics, weights):
    """Replay value: mostly the same drivers as fun, plus variety (no dominant line) and lead changes."""
    s = weighted(metrics, weights)
    return round(1 + 4 * (0.6 * s + 0.2 * metrics.get("dominant_strategy_absent", 0) + 0.2 * metrics.get("lead_changes", 0)), 2)


def would_buy(fun, minutes, tolerance, preferred):
    """('yes'|'maybe'|'no', price). Price sits in the persona's tolerance band, higher for better fun and longer games."""
    verdict = "yes" if fun >= 3.8 else "maybe" if fun >= 3.0 else "no"
    if verdict == "no":
        return verdict, None
    lo, hi = tolerance
    q = clamp((fun - 3.0) / 2.0) * clamp(minutes / max(preferred[0], 1))
    return verdict, int(round(lo + (hi - lo) * q))


# Pet-peeve keywords -> a test on the metrics. A peeve is "hit" when its title matches a keyword and the test is true.
PEEVE_TESTS = [
    (r"rulebook|rules overhead|hard to teach|ambiguous rules|dense", lambda m, r: m["rules_simplicity"] < 0.5),
    (r"downtime|analysis paralysis|waiting", lambda m, r: r.get("downtime", 0) > 4),
    (r"long playtime|long game|overstay|bloated", lambda m, r: r.get("minutes", 0) > r.get("preferred_max", 1e9) * 1.0 and m["length_fit"] < 0.5),
    (r"luck", lambda m, r: m["skill_expression"] < 0.5),
    (r"dominant|solved|single solved", lambda m, r: m["dominant_strategy_absent"] < 0.7),
    (r"runaway|hopelessly behind|rubber", lambda m, r: m["catch_up"] < 0.5),
    (r"solitaire", lambda m, r: m["interaction"] < 0.2),
    (r"take-that|stealing", lambda m, r: m["interaction"] > 0.8),
    (r"first-player|turn order", lambda m, r: r.get("seat_gap", 0) > 5),
]


def peeves_hit(titles, metrics, raw):
    hit = []
    for t in titles:
        for pat, test in PEEVE_TESTS:
            if re.search(pat, t, re.I) and test(metrics, raw):
                hit.append(t.rstrip(".").split(".")[0].strip())
                break
    return hit


def check_veto(rules, fun, metrics, seat_gap):
    """The Bar Raiser's veto: returns {"active": bool, "reasons": [...]} from the limits in the persona's `veto` block."""
    reasons = []
    if fun < rules.get("min_fun", 0):
        reasons.append("predicted fun %.2f is below %.1f" % (fun, rules["min_fun"]))
    if metrics.get("dominant_strategy_absent", 1) < rules.get("min_dominant_strategy_absent", 0):
        reasons.append("a dominant strategy was flagged by the playtester")
    if seat_gap > rules.get("max_seat_gap", 1e9):
        reasons.append("seat advantage of %.1f points" % seat_gap)
    if "originality" in metrics and metrics["originality"] < rules.get("min_originality", 0):
        reasons.append("low originality in the brief's rubric")
    return {"active": bool(reasons), "reasons": reasons}


def summarise(personas_out):
    funs = {k: v["fun"] for k, v in personas_out.items()}
    if not funs:
        return {}
    best, worst = max(funs, key=funs.get), min(funs, key=funs.get)
    out = {"average_fun": round(sum(funs.values()) / len(funs), 2),
           "spread": round(max(funs.values()) - min(funs.values()), 2), "best_fit": best, "worst_fit": worst}
    vetoes = {k: v["veto"]["reasons"] for k, v in personas_out.items() if v.get("veto", {}).get("active")}
    if vetoes:
        out["veto"] = vetoes
    return out


# ---------------------------------------------------------------- the whole file
def build_panel(playtest, rules_words, results, personas, revision=1, previous=None, brief=None):
    """results: contents of sim/panel-results.json. Returns the panel.json dict."""
    minutes = (playtest.get("length") or {}).get("estimated_minutes") or 0
    out = {}
    for pid, per in results["personas"].items():
        p = personas[pid]
        raw = per["raw"]
        metrics = {**game_metrics(playtest, rules_words, p["preferred_minutes"], brief), **bot_metrics(raw)}
        fun = fun_from_metrics(metrics, p["weights"])
        buy, price = would_buy(fun, minutes, p["price_tolerance_usd"], p["preferred_minutes"])
        raw = {**raw, "seat_gap": playtest.get("seat_balance_gap", 0), "minutes": minutes, "preferred_max": p["preferred_minutes"][1]}
        out[pid] = {
            "fun": fun, "replay": replay_from_metrics(metrics, p["weights"]), "would_buy": buy, "price_usd": price,
            "metrics": {k: round(v, 3) for k, v in metrics.items()},
            "pet_peeves_hit": peeves_hit(p["peeves"], metrics, raw),
            "bot": per["bot"], "best_table": per.get("best_table"), "worst_table": per.get("worst_table"),
            "review": ((previous or {}).get("personas", {}).get(pid, {}) or {}).get("review"),
        }
        if p.get("veto"):
            out[pid]["veto"] = check_veto(p["veto"], fun, metrics, playtest.get("seat_balance_gap", 0))
    matchups = []
    for m in results.get("matchups", []):
        a, b = m["a"], m["b"]
        matchups.append({**m, "a_fun": fun_from_metrics({**game_metrics(playtest, rules_words, personas[a]["preferred_minutes"], brief), **bot_metrics(m["a_raw"])}, personas[a]["weights"]),
                         "b_fun": fun_from_metrics({**game_metrics(playtest, rules_words, personas[b]["preferred_minutes"], brief), **bot_metrics(m["b_raw"])}, personas[b]["weights"])})
        matchups[-1].pop("a_raw"); matchups[-1].pop("b_raw")
    return {"revision": revision, "stage": "scores", "personas": out, "rotation": results["rotation"],
            "matchups": matchups, "summary": summarise(out)}


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    slug = argv[0]
    revision = int(argv[argv.index("--revision") + 1]) if "--revision" in argv else None
    g = os.path.join(ROOT, "games", slug)
    playtest = json.load(open(os.path.join(g, "playtest.json")))
    words = len(open(os.path.join(g, "rules.md"), encoding="utf-8").read().split())
    results = json.load(open(os.path.join(g, "sim", "panel-results.json")))
    prev_path = os.path.join(g, "panel.json")
    previous = json.load(open(prev_path)) if os.path.exists(prev_path) else None
    brief_path = os.path.join(g, "brief.json")
    brief = json.load(open(brief_path)) if os.path.exists(brief_path) else None
    panel = build_panel(playtest, words, results, load_personas(ROOT, set(results["personas"])),
                        revision or playtest.get("revision", 1), previous, brief)
    with open(prev_path, "w") as f:
        json.dump(panel, f, indent=2)
        f.write("\n")
    s = panel["summary"]
    print("wrote %s: average fun %.2f, spread %.2f, best fit %s, worst fit %s" % (prev_path, s["average_fun"], s["spread"], s["best_fit"], s["worst_fit"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
