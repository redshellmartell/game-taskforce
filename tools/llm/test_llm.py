import json, os, sys, unittest
from unittest import mock
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import llm

CFG = {"jobs": {"persona_review": {"provider": "ollama", "model": "m"}, "x": {"provider": "openrouter", "model": "f:free"}}}

class T(unittest.TestCase):
    def test_config_file_is_valid_and_has_no_keys(self):
        c = llm.load_config()
        for job in ("persona_review", "persona_chat", "research_summary"): self.assertIn(job, c["jobs"])
        self.assertNotRegex(json.dumps(c), r"sk-|AIza|api[_-]?key\"\s*:")
    def test_ollama_call_shape(self):
        with mock.patch.object(llm, "_post", return_value={"message": {"content": "hi"}}) as p:
            r = llm.ask("persona_review", "prompt", system="s", config=CFG)
        self.assertEqual(r["text"], "hi"); self.assertEqual(r["provider"], "ollama")
        url, body = p.call_args[0][0], p.call_args[0][1]
        self.assertTrue(url.endswith("/api/chat")); self.assertEqual(body["messages"][0]["role"], "system"); self.assertFalse(body["stream"])
    def test_free_api_blocked_without_approval(self):
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "k"}, clear=False):
            os.environ.pop("FREE_API_APPROVED", None)
            with self.assertRaises(llm.LLMError) as e: llm.ask("x", "secret design", config=CFG)
        self.assertIn("free-api", str(e.exception))
    def test_free_api_allowed_when_approved_or_not_private(self):
        out = {"choices": [{"message": {"content": "ok"}}]}
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "k", "FREE_API_APPROVED": "1"}), mock.patch.object(llm, "_post", return_value=out):
            self.assertEqual(llm.ask("x", "p", config=CFG)["text"], "ok")
        with mock.patch.dict(os.environ, {"OPENROUTER_API_KEY": "k"}), mock.patch.object(llm, "_post", return_value=out):
            self.assertEqual(llm.ask("x", "public text", config=CFG, private=False)["text"], "ok")
    def test_missing_key_message_names_variable_only(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(llm.LLMError) as e: llm.call_provider("anthropic", "m", "p")
        self.assertIn("ANTHROPIC_API_KEY", str(e.exception))
    def test_unknown_provider_and_job(self):
        with self.assertRaises(llm.LLMError): llm.call_provider("nope", "m", "p")
        with self.assertRaises(llm.LLMError): llm.ask("missing", "p", config=CFG)
    def test_google_and_anthropic_parse(self):
        with mock.patch.dict(os.environ, {"GOOGLE_API_KEY": "k", "ANTHROPIC_API_KEY": "k"}):
            with mock.patch.object(llm, "_post", return_value={"candidates": [{"content": {"parts": [{"text": "a"}, {"text": "b"}]}}]}):
                self.assertEqual(llm.call_provider("google", "gemini", "p"), "ab")
            with mock.patch.object(llm, "_post", return_value={"content": [{"type": "text", "text": "c"}]}):
                self.assertEqual(llm.call_provider("anthropic", "m", "p"), "c")

if __name__ == "__main__": unittest.main()
