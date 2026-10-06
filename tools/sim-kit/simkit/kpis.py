"""KPI targets (from CLAUDE.md) and the playtest.json writer, so every playtest reports the same keys."""
TARGETS = dict(seat_gap_max=5.0, skill_gap_min=20.0, length_tolerance=0.20, runaway_max=0.65, lead_changes_min=2.0,
               dead_cards_max=0, ambiguities_max=0)


def evaluate(summary, skill_gap_pts, target_minutes, estimated_minutes, dead_cards=0, ambiguities=0, targets=None):
    """Returns a list of (name, value, target, passed). None values (not measured) are reported as not passed."""
    t = dict(TARGETS, **(targets or {}))
    rows = []
    def add(name, value, target, ok): rows.append((name, value, target, bool(ok) if value is not None else False))
    add("seat gap (pts)", summary["seat_gap"], f"<= {t['seat_gap_max']}", summary["seat_gap"] <= t["seat_gap_max"])
    add("strategic vs random gap (pts)", skill_gap_pts, f">= {t['skill_gap_min']}", skill_gap_pts is not None and skill_gap_pts >= t["skill_gap_min"])
    lo, hi = target_minutes * (1 - t["length_tolerance"]), target_minutes * (1 + t["length_tolerance"])
    add("length (min)", estimated_minutes, f"{lo:.1f}-{hi:.1f}", lo <= estimated_minutes <= hi)
    rl = summary["runaway_leader_rate"]
    add("runaway leader rate", rl, f"<= {t['runaway_max']}", rl is not None and rl <= t["runaway_max"])
    lc = summary["lead_changes_mean"]
    add("lead changes per game", lc, f">= {t['lead_changes_min']}", lc is not None and lc >= t["lead_changes_min"])
    add("dead cards", dead_cards, f"<= {t['dead_cards_max']}", dead_cards <= t["dead_cards_max"])
    add("ambiguities", ambiguities, f"<= {t['ambiguities_max']}", ambiguities <= t["ambiguities_max"])
    return rows


def to_playtest_json(summary, bot_win_rates, skill_gap_pts, target_minutes, estimated_minutes, verdict, revision,
                     cards=None, ambiguities=None, problems=None, previous=None, bots_only=True):
    """Same keys as the existing games/*/playtest.json files (the dashboard reads them)."""
    out = {"verdict": verdict, "revision": revision, "games_simulated": summary["games"],
           "seat_win_rates": {str(i + 1): r for i, r in enumerate(summary["seat_win_rates"])},
           "seat_balance_gap": summary["seat_gap"], "bot_win_rates": bot_win_rates, "skill_expression": skill_gap_pts,
           "length": dict(mean_turns=summary["length"]["mean_turns"], stdev=summary["length"]["stdev"],
                          estimated_minutes=estimated_minutes, target_minutes=target_minutes),
           "length_histogram": summary["length_histogram"], "ties": summary["ties"], "turn_cap_hits": summary["turn_cap_hits"],
           "lead_changes_mean": summary["lead_changes_mean"], "runaway_leader_rate": summary["runaway_leader_rate"],
           "cards": cards or [], "ambiguities": ambiguities or [], "problems": problems or []}
    if previous: out["previous"] = previous
    if bots_only: out["validation"] = "bots only, unvalidated"
    return out
