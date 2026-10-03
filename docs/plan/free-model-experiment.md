# Free-model experiment (task 009)

**Status: not run yet.** This session ran in the cloud, which has no Ollama, no free-API keys, and cannot read the providers' terms. What exists is the tooling (`tools/llm/`); the results below are filled in after the comparison runs on the owner's Mac.

## Setup
- Jobs: persona reviews (5 for Duel Flip, same inputs as task 006), research-page summaries (3 evidence files).
- Candidates (in `tools/llm/config.json`): Haiku baseline, Ollama small (`llama3.1:8b`), Ollama mid (`qwen2.5:14b`), one OpenRouter free model (only with approval `free-model-experiment-api`).
- Scoring: one neutral Sonnet pass scores each blind output 1-5 on in character, grounded in the game data, specific and useful, names a real frustration.

## Results
| Candidate | In character | Grounded | Specific | Real frustration | Seconds per review |
|---|---|---|---|---|---|
| (not run) | | | | | |

## Privacy notes
Local Ollama keeps everything on the Mac. For any free API the provider's data-use terms must be read and the owner must approve first (`free-api` gate); not done.

## Recommendation
None yet. The existing Haiku reviews (task 006) cost about 34-42k tokens each, so even a perfect free model would save only a small share of the plan. Question for the owner after the run: "Switch persona work to X?"
