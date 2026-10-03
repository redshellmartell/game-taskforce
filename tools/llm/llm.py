#!/usr/bin/env python3
"""One small switch for sending a prompt to a language model (standard library only).

Providers (set per job in tools/llm/config.json):
  anthropic   Claude (baseline, e.g. claude-haiku-4-5-20251001). Key in env ANTHROPIC_API_KEY.
  ollama      A model running on this computer (http://localhost:11434). No key; nothing leaves the machine.
  openrouter  OpenRouter ":free" models. Key in env OPENROUTER_API_KEY.
  google      Google AI Studio (Gemini free tier). Key in env GOOGLE_API_KEY.
Keys are read only from environment variables and are never written to any file.

Privacy: unpublished game designs must not go to a free API without the owner's `free-api` approval.
`ask(..., private=True)` (the default) refuses openrouter and google unless env FREE_API_APPROVED=1 is set.

Usage:  python3 tools/llm/llm.py <job> "<prompt>"        (job = persona_review | persona_chat | research_summary)
        python3 tools/llm/llm.py --provider ollama --model llama3.1:8b "<prompt>"
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = {"anthropic": "ANTHROPIC_API_KEY", "openrouter": "OPENROUTER_API_KEY", "google": "GOOGLE_API_KEY"}
FREE_APIS = {"openrouter", "google"}


class LLMError(RuntimeError):
    pass


def load_config(path=None):
    with open(path or os.path.join(HERE, "config.json"), encoding="utf-8") as f:
        return json.load(f)


def _post(url, body, headers, timeout=180):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise LLMError("%s returned HTTP %d: %s" % (url.split("?")[0], e.code, e.read().decode()[:200]))
    except (urllib.error.URLError, TimeoutError) as e:
        raise LLMError("could not reach %s: %s" % (url.split("?")[0], e))


def _key(provider):
    k = os.environ.get(KEYS[provider])
    if not k:
        raise LLMError("set the environment variable %s (never put the key in a file)" % KEYS[provider])
    return k


def call_provider(provider, model, prompt, system=None, max_tokens=800, base_url=None):
    """Returns the model's text. Raises LLMError with a plain message."""
    if provider == "anthropic":
        body = {"model": model, "max_tokens": max_tokens, "messages": [{"role": "user", "content": prompt}]}
        if system:
            body["system"] = system
        out = _post("https://api.anthropic.com/v1/messages", body, {"x-api-key": _key(provider), "anthropic-version": "2023-06-01"})
        return "".join(b.get("text", "") for b in out.get("content", []))
    if provider == "ollama":
        msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
        out = _post((base_url or "http://localhost:11434") + "/api/chat", {"model": model, "messages": msgs, "stream": False, "options": {"num_predict": max_tokens, "num_ctx": 16384}}, {}, timeout=600)
        return out["message"]["content"]
    if provider == "openrouter":
        msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
        out = _post("https://openrouter.ai/api/v1/chat/completions", {"model": model, "messages": msgs, "max_tokens": max_tokens}, {"Authorization": "Bearer " + _key(provider)})
        return out["choices"][0]["message"]["content"]
    if provider == "google":
        body = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"maxOutputTokens": max_tokens}}
        if system:
            body["systemInstruction"] = {"parts": [{"text": system}]}
        out = _post("https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s" % (model, _key(provider)), body, {})
        return "".join(p.get("text", "") for p in out["candidates"][0]["content"]["parts"])
    raise LLMError("unknown provider %r (use anthropic, ollama, openrouter or google)" % provider)


def ask(job, prompt, system=None, config=None, private=True, provider=None, model=None, max_tokens=800):
    """Run one job with the provider and model from config.json (or an override). Returns {text, provider, model, seconds}."""
    cfg = config or load_config()
    j = cfg["jobs"].get(job, {}) if job else {}
    provider, model = provider or j.get("provider"), model or j.get("model")
    if not provider or not model:
        raise LLMError("job %r has no provider/model in config.json" % job)
    if private and provider in FREE_APIS and os.environ.get("FREE_API_APPROVED") != "1":
        raise LLMError("blocked: %s is a free third-party API and this prompt contains unpublished game content. Get the owner's `free-api` approval, then set FREE_API_APPROVED=1." % provider)
    t = time.time()
    text = call_provider(provider, model, prompt, system, max_tokens, cfg.get("ollama_url"))
    return {"text": text, "provider": provider, "model": model, "seconds": round(time.time() - t, 1)}


def main(argv):
    provider = model = None
    args = list(argv)
    for flag in ("--provider", "--model"):
        if flag in args:
            i = args.index(flag)
            val = args[i + 1]
            del args[i:i + 2]
            provider, model = (val, model) if flag == "--provider" else (provider, val)
    if not args:
        print(__doc__)
        return 2
    job, prompt = (None, args[0]) if (provider or model) else (args[0], " ".join(args[1:]))
    try:
        r = ask(job, prompt, provider=provider, model=model)
    except LLMError as e:
        print("error:", e)
        return 1
    print(r["text"])
    print("\n[%s %s, %.1fs]" % (r["provider"], r["model"], r["seconds"]), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
