from dataclasses import dataclass
import os
import httpx

@dataclass
class ModelResult:
    text: str
    provider: str

class LLMProvider:
    def generate(self, instruction: str) -> ModelResult:
        raise NotImplementedError

class OpenAICompatibleProvider(LLMProvider):
    def __init__(self):
        self.base_url=os.getenv("LLM_BASE_URL","https://api.openai.com/v1").rstrip("/")
        self.api_key=os.getenv("LLM_API_KEY","")
        self.model=os.getenv("LLM_MODEL","gpt-5-mini")

    def generate(self, instruction: str) -> ModelResult:
        if not self.api_key:
            return ModelResult("Demo mode: no LLM_API_KEY is configured. The engineering prompt was prepared successfully. Configure a compatible provider to generate a model response.","demo")
        r=httpx.post(f"{self.base_url}/chat/completions",headers={"Authorization":f"Bearer {self.api_key}","Content-Type":"application/json"},json={"model":self.model,"messages":[{"role":"user","content":instruction}],"temperature":0.2},timeout=60)
        r.raise_for_status()
        return ModelResult(r.json()["choices"][0]["message"]["content"],"openai-compatible")

def get_provider()->LLMProvider:
    return OpenAICompatibleProvider()
