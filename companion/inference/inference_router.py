"""
Module: inference_router

This module handles LLM inference with support for GPT-4o, Claude Sonnet, and LLaMA models.
"""

from anthropic import Anthropic
import openai
import requests
import os

OPENAI_PROVIDER = "openai"
ANTHROPIC_PROVIDER = "anthropic"
LOCAL_PROVIDER = "local"

GPT_4O_MODEL = "gpt-4o"
CLAUDE_SONNET_MODEL = "claude-sonnet-4-20250514"
LLAMA3_8B_MODEL = "llama3-8b"

SUPPORTED_MODELS = [GPT_4O_MODEL, CLAUDE_SONNET_MODEL, LLAMA3_8B_MODEL]

DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 512

class InferenceRouter:
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    def _call_openai(self, prompt: str, model: str = GPT_4O_MODEL, temperature: float = DEFAULT_TEMPERATURE, max_tokens: int = DEFAULT_MAX_TOKENS) -> str:
        """
        Call the OpenAI API with the given prompt and parameters.
        """
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message["content"].strip()
    
    def _call_anthropic(self, prompt: str, model: str = CLAUDE_SONNET_MODEL, temperature: float = DEFAULT_TEMPERATURE, max_tokens: int = DEFAULT_MAX_TOKENS) -> str:
        """
        Call the Anthropic API with the given prompt and parameters.
        """
        client = Anthropic(api_key=self.anthropic_key)
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # print(response.content[0].text)

        # Claude’s response is in `response.content` (list of message blocks)
        return response.content[0].text.strip() if response.content else "[No response received]"

    def _call_llama(self, prompt: str, model: str = LLAMA3_8B_MODEL, temperature: float = DEFAULT_TEMPERATURE, max_tokens: int = DEFAULT_MAX_TOKENS) -> str:
        """
        Call the LLaMA API with the given prompt and parameters.
        """
        response = requests.post("http://localhost:8000/infer", json={"prompt": prompt, "temperature": temperature, "max_tokens": max_tokens})
        return response.json().get("text", "")

    def prompt(self, prompt: str, model: str, provider:str = OPENAI_PROVIDER) -> str:
        """
        Prompt the specified LLM with the given prompt.

        :param prompt: The full prompt ready for the LLM.
        :param model: The model to use for inference (default is "gpt-4o").
        :param provider: The provider to use for inference (default is "openai").
        :param temperature: The temperature setting for the model (default is 0.7).
        :param max_tokens: The maximum number of tokens to generate (default is 512).
        :return: The output string from the model.
        """
        if model not in SUPPORTED_MODELS:
            raise ValueError(f"Unsupported model specified: {model}. Supported models: {', '.join(SUPPORTED_MODELS)}")
        
        if provider not in [OPENAI_PROVIDER, ANTHROPIC_PROVIDER]:
            raise ValueError(f"Unsupported provider: {provider}. Supported providers: {OPENAI_PROVIDER}, {ANTHROPIC_PROVIDER}")
        
        try:
            if provider == OPENAI_PROVIDER:
                return self._call_openai(prompt, model, temperature = DEFAULT_TEMPERATURE, max_tokens = DEFAULT_MAX_TOKENS)
            elif provider == ANTHROPIC_PROVIDER:
                return self._call_anthropic(prompt, model, temperature = DEFAULT_TEMPERATURE, max_tokens = DEFAULT_MAX_TOKENS)
            elif provider == LOCAL_PROVIDER:
                return self._call_llama(prompt, model, temperature = DEFAULT_TEMPERATURE, max_tokens = DEFAULT_MAX_TOKENS)
            else:
                raise ValueError(f"Unsupported provider: {provider}. Supported providers: {OPENAI_PROVIDER}, {ANTHROPIC_PROVIDER}, {LOCAL_PROVIDER}")
        except openai.error.RateLimitError:
            print(f"Rate limit exceeded for {model}, attempting fallback...")
            return self.prompt(prompt, model=CLAUDE_SONNET_MODEL, provider=ANTHROPIC_PROVIDER)
        except Exception as ex:
            print(f"Error during inference: {ex}")
            return ""  # Return an empty string or handle as needed

