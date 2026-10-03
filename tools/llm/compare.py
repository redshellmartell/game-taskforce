#!/usr/bin/env python3
"""Blind comparison of language-model providers on persona reviews and research summaries (task 009).

Run on the owner's Mac (where Ollama runs):
  python3 tools/llm/compare.py --game duelflip --candidates haiku-baseline,ollama-small
Writes experiments/free-models/<candidate>/<persona>.md, timings.json, and a BLIND bundle
(experiments/free-models/blind/review-<persona>-<label>.md plus key.json, which hides which candidate wrote which).
A neutral Claude pass then scores the blind files; the key is only opened afterwards.
--dry-run builds and shows the prompt sizes without calling any model.
Candidates that use a free API need the owner's `free-api` approval (set FREE_API_APPROVED=1).
"""
import argparse, json, os, random, re, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import llm

OUT = os.path.join(ROOT, "experiments", "free-models")
SYSTEM = open(os.path.join(ROOT, ".claude", "agents", "panel-player.md"), encoding="utf-8").read().split("---", 2)[2].strip()
HEADINGS = "First impression; Best moment and worst moment; Confusing rules; Pet peeves hit; Who I enjoyed playing with; Ratings (fun, replay, would buy with USD price); The one change I'd make; Who I'd recommend this to"

def read(p):
    return open(os.path.join(ROOT, p), encoding="utf-8").read()

def review_prompt(game, persona):
    """The same inputs the panel-player agent gets in task 006, pasted in (a plain model cannot open files)."""
    panel = json.load(open(os.path.join(ROOT, "games", game, "panel.json")))["personas"][persona]
    panel = {k: v for k, v in panel.items() if k != "review"}
    logs = "\n\n".join("LOG %d:\n%s" % (i, read("games/%s/sim/logs/%s-%d.txt" % (game, persona, i))) for i in (1, 2))
    return ("Write the review described in your instructions, in the persona's voice, under 350 words, with these headings: %s.\n\n"
            "=== PERSONA PROFILE ===\n%s\n\n=== EVIDENCE ===\n%s\n\n=== RULES ===\n%s\n\n=== YOUR PREDICTED SCORES (from simulation) ===\n%s\n\n=== SAMPLE GAME LOGS ===\n%s\n"
            % (HEADINGS, read("panel/personas/%s.md" % persona), read("panel/evidence/%s.md" % persona), read("games/%s/rules.md" % game), json.dumps(panel, indent=1), logs))

def summary_prompt(path):
    return "Summarise this research page in at most 150 words: the main themes, and the three most useful findings for a board game designer. Do not add facts that are not in it.\n\n" + read(path)

def run(cands, jobs, dry):
    cfg = llm.load_config(); by = {c["name"]: c for c in cfg["candidates"]}
    timings, results = [], {}
    for name in cands:
        c = by[name]
        for kind, key, prompt in jobs:
            if dry:
                print("%s %s %s: prompt %d characters" % (name, kind, key, len(prompt))); continue
            try:
                r = llm.ask(None, prompt, system=SYSTEM if kind == "review" else None, provider=c["provider"], model=c["model"], max_tokens=900)
            except llm.LLMError as e:
                print("%s %s %s FAILED: %s" % (name, kind, key, e)); timings.append({"candidate": name, "kind": kind, "item": key, "error": str(e)}); continue
            d = os.path.join(OUT, name); os.makedirs(d, exist_ok=True)
            open(os.path.join(d, "%s-%s.md" % (kind, key)), "w", encoding="utf-8").write(r["text"])
            results[(name, kind, key)] = r["text"]
            timings.append({"candidate": name, "kind": kind, "item": key, "seconds": r["seconds"], "words": len(r["text"].split())})
            print("%s %s %s: %.1fs, %d words" % (name, kind, key, r["seconds"], len(r["text"].split())))
    return timings, results

def blind(results):
    """Copy each output to blind/<kind>-<item>-<label>.md with shuffled labels; the key stays in key.json."""
    rng = random.Random(1); key = {}
    os.makedirs(os.path.join(OUT, "blind"), exist_ok=True)
    groups = {}
    for (cand, kind, item), text in results.items(): groups.setdefault((kind, item), []).append((cand, text))
    for (kind, item), outs in groups.items():
        rng.shuffle(outs)
        for i, (cand, text) in enumerate(outs):
            label = "ABCDEFGH"[i]
            open(os.path.join(OUT, "blind", "%s-%s-%s.md" % (kind, item, label)), "w", encoding="utf-8").write(text)
            key["%s-%s-%s" % (kind, item, label)] = cand
    json.dump(key, open(os.path.join(OUT, "blind", "key.json"), "w"), indent=1)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--game", default="duelflip"); ap.add_argument("--candidates", required=True)
    ap.add_argument("--summaries", default="panel/evidence/strategist.md,panel/evidence/casual.md,panel/evidence/family.md"); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    personas = sorted(re.sub(r"\.md$", "", f) for f in os.listdir(os.path.join(ROOT, "panel", "personas")) if f.endswith(".md"))
    jobs = [("review", p, review_prompt(a.game, p)) for p in personas] + [("summary", os.path.basename(s)[:-3], summary_prompt(s)) for s in a.summaries.split(",") if s]
    timings, results = run(a.candidates.split(","), jobs, a.dry_run)
    if not a.dry_run:
        os.makedirs(OUT, exist_ok=True); json.dump(timings, open(os.path.join(OUT, "timings.json"), "w"), indent=1); blind(results)
        print("Done. Next: ask Claude Code to score the files in experiments/free-models/blind/ without opening key.json.")

if __name__ == "__main__":
    main()
