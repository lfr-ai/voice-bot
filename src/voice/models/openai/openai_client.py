# type: ignore
from typing import Any

from openai import AzureOpenAI

from voice.config.config import Config


class OpenAIClient:
    """
    Client for interacting with the OpenAI API.
    """

    def __init__(self, cfg: Config):
        """
        Initialize the OpenAIClient.

        Args:
            cfg (Config): Configuration object containing settings.
        """
        self.client = AzureOpenAI(
            api_key=cfg.OPENAI_KEY,
            api_version=cfg.OPENAI_VERSION,
            azure_endpoint=cfg.OPENAI_ENDPOINT,
        )

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
        temperature: float,
        max_completion_tokens: int,
        **kwargs: Any
    ) -> str:
        """
        Send a chat request to OpenAI and return the assistant's response.

        Args:
            system_prompt (str): Prompt defining assistant behavior.
            user_prompt (str): User's prompt to the assistant.
            model (str): Name of the OpenAI model.
            temperature (float): Sampling temperature for the response variability.
            max_completion_tokens (int): Maximum number of tokens in the response.
            **kwargs (Any): Optional keyword arguments passed to the chat request.
        """
        messages = [
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
            {"role": " user", "content": [{"type": "text", "text": user_prompt}]},
        ]
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=max_completion_tokens,
            **kwargs
        )
        return response.choices[0].message.content
