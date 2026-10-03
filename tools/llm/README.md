# Free-model experiment (task 009)

Question: can the high-volume, low-stakes AI work (persona reviews, persona chat, research summaries) run on a free model instead of the Claude subscription? Design, simulation and critique stay on Claude.

**What is here:** `llm.py` (one switch for Claude, Ollama on your Mac, OpenRouter free models, Google AI Studio), `config.json` (which model each job uses; all on Haiku for now), `compare.py` (blind comparison on Duel Flip), `test_llm.py`. Keys come from environment variables only; nothing secret is stored in the repository. Free APIs are blocked for game content unless you set `FREE_API_APPROVED=1` after approving the `free-api` request.

## Run it on your Mac (local models keep everything on the Mac)
1. Check what your Mac can run: `sysctl -n machdep.cpu.brand_string`, `sysctl -n hw.memsize` (bytes), `df -h ~`. About 16 GB memory: small models (7-9B). 32 GB or more: mid-size (14-32B).
2. Install Ollama (ollama.com), then pull a model: `ollama pull llama3.1:8b` (16 GB Macs) or `ollama pull qwen2.5:14b` (32 GB+).
3. In the repository folder: `python3 tools/llm/compare.py --candidates ollama-small` (add `haiku-baseline` too if you have `ANTHROPIC_API_KEY` set; otherwise the Claude baseline is the existing reviews in `games/duelflip/panel/`).
4. Then tell Claude Code: "score the blind files in experiments/free-models/blind" (a Sonnet pass that does not see which model wrote which).
