"""simkit: shared simulation helpers for the playtester (standard library only).
A game adapter is one function  play(bots, seed) -> result dict  with keys:
  winner   seat index of the winner, or None for a tie
  turns    number of turns played
  capped   True if the turn cap ended the game
  leaders  optional list: seat index leading after each turn (None when level); use leaders_from_diff() for 2 players
See README.md. The numbers here follow the KPI targets in CLAUDE.md."""
from .stats import (wilson, leaders_from_diff, lead_changes, summarize, run_match, round_robin, ablation, mean, stdev)
from .kpis import TARGETS, evaluate, to_playtest_json

from .parallel import run_match_parallel
