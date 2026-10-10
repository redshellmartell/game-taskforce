"""Parallel match runner (standard library: multiprocessing, fork start method on Linux/macOS).
run_match_parallel gives the same rows as stats.run_match for the same seeds, just spread over CPU cores.
play and makers may be lambdas or closures: they are inherited by the worker processes through fork, not pickled.
Rows must be picklable: pass `keep` to choose which keys of play()'s result to send back (drop big objects such as the final state),
or `post(result, order) -> dict` to turn each result into a small row inside the worker (extra per-game stats go here)."""
import multiprocessing as mp

_JOB = {}


def _one(i):
    j = _JOB; k = len(j["makers"])
    order = [(x + i) % k for x in range(k)] if j["rotate"] else list(range(k))
    bots = [j["makers"][order[s]](j["seed"] + i * 7 + s) for s in range(k)]
    res = j["play"](bots, j["seed"] + i)
    r = j["post"](res, order) if j["post"] else {key: res[key] for key in j["keep"] if key in res}
    r = dict(r); r["order"] = order
    return r


def run_match_parallel(play, makers, n, seed=0, rotate=True, workers=None, keep=("winner", "turns", "capped", "leaders"), post=None):
    """Same contract as stats.run_match (rows carry 'order'), computed on `workers` processes (default: all cores)."""
    workers = workers or mp.cpu_count()
    _JOB.clear(); _JOB.update(play=play, makers=makers, seed=seed, rotate=rotate, keep=keep, post=post)
    if workers <= 1 or "fork" not in mp.get_all_start_methods():
        return [_one(i) for i in range(n)]
    with mp.get_context("fork").Pool(workers) as pool:
        return pool.map(_one, range(n), chunksize=max(1, n // (workers * 8)))
