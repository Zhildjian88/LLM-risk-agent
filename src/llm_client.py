"""
src/llm_client.py
Provider-flexible LLM wrapper.
Retry with exponential backoff on overload and rate limit errors.
"""

import os
import time
import config

class LLMClient:
    def __init__(self, provider: str = None, model: str = None):
        self.provider = provider or config.LLM_PROVIDER
        self.model = model or config.LLM_MODEL

    def generate(self, prompt: str) -> tuple:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                start = time.perf_counter()
                if self.provider == "anthropic":
                    text = self._call_anthropic(prompt)
                elif self.provider == "openai":
                    text = self._call_openai(prompt)
                else:
                    raise ValueError(f"Unsupported provider: {self.provider}")
                text = self._clean_response(text)
                latency_ms = (time.perf_counter() - start) * 1000
                return text, latency_ms
            except Exception as e:
                if any(term in str(e).lower() for term in ["overloaded", "rate", "429", "529"]):
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        print(f"   ⚠️ Retrying in {wait_time}s (attempt {attempt+1})")
                        time.sleep(wait_time)
                    else:
                        raise
                else:
                    raise

    def _clean_response(self, text: str) -> str:
        text = text.strip()
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()
        return text

    def _call_anthropic(self, prompt: str) -> str:
        if "ANTHROPIC_API_KEY" not in os.environ:
            raise EnvironmentError("ANTHROPIC_API_KEY not set")
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        response = client.messages.create(
            model=self.model,
            max_tokens=512,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def _call_openai(self, prompt: str) -> str:
        if "OPENAI_API_KEY" not in os.environ:
            raise EnvironmentError("OPENAI_API_KEY not set")
        from openai import OpenAI
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model=self.model,
            temperature=0,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
