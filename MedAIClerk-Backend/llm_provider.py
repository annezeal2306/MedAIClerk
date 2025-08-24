import os
from typing import Optional
import logging

LLM_MODE = os.getenv("LLM_MODE", "api").lower()
OSS_MODEL_ID = os.getenv("OSS_MODEL_ID", "openai/gpt-oss-20b")
OSS_DEVICE = os.getenv("OSS_DEVICE", "cpu")
OSS_MAX_NEW_TOKENS = int(os.getenv("OSS_MAX_NEW_TOKENS", "512"))
OSS_TEMPERATURE = float(os.getenv("OSS_TEMPERATURE", "0.2"))
OSS_QUANT = os.getenv("OSS_QUANT", "").lower()  # "", "4bit", "8bit"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

logger = logging.getLogger("llm_provider")

class LLM:
    def __init__(self):
        self.mode = LLM_MODE
        self._api_client = None
        self._hf_model = None
        self._hf_tokenizer = None
        if self.mode == "oss":
            self._init_oss()
        else:
            self._init_api()

    def _init_api(self):
        try:
            from openai import OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise RuntimeError("OPENAI_API_KEY is missing for API mode.")
            self._api_client = OpenAI(api_key=api_key)
        except Exception as e:
            raise RuntimeError(f"Failed to init OpenAI API client: {e}")

    def _init_oss(self):
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
            self._hf_tokenizer = AutoTokenizer.from_pretrained(OSS_MODEL_ID, use_fast=True)
            torch_dtype = torch.bfloat16 if OSS_DEVICE == "cuda" else torch.float32
            self._hf_model = AutoModelForCausalLM.from_pretrained(
                OSS_MODEL_ID,
                torch_dtype=torch_dtype,
                device_map="auto" if OSS_DEVICE == "cuda" else None
            )
            if OSS_DEVICE == "cuda":
                self._hf_model = self._hf_model.to("cuda")
        except Exception as e:
            raise RuntimeError(f"Failed to init OSS model '{OSS_MODEL_ID}': {e}")

    def generate(self, prompt: str) -> str:
        if self.mode == "oss":
            return self._gen_oss(prompt)
        else:
            return self._gen_api(prompt)

    def _gen_api(self, prompt: str) -> str:
        try:
            resp = self._api_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=OSS_TEMPERATURE,
            )
            return resp.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI API generation failed: {e}")

    def _gen_oss(self, prompt: str) -> str:
        try:
            import torch
            tok = self._hf_tokenizer
            model = self._hf_model
            inputs = tok(prompt, return_tensors="pt")
            if OSS_DEVICE == "cuda":
                inputs = {k: v.to("cuda") for k, v in inputs.items()}
            output_ids = model.generate(
                **inputs,
                max_new_tokens=OSS_MAX_NEW_TOKENS,
                do_sample=False,
                temperature=OSS_TEMPERATURE,
                pad_token_id=tok.eos_token_id,
                eos_token_id=tok.eos_token_id,
            )
            text = tok.decode(output_ids[0], skip_special_tokens=True)
            return text[len(prompt):].strip() if text.startswith(prompt) else text
        except Exception as e:
            raise RuntimeError(f"OSS generation failed: {e}")
