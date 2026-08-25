"""DeepSeek provider implementation."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING
from ariba.providers.openai import OpenAIProvider

if TYPE_CHECKING:
    from pathlib import Path


class DeepSeekProvider(OpenAIProvider):
    """DeepSeek API provider."""

    def __init__(self) -> None:
        self.api_key = os.getenv("DEEPSEEK_API_KEY", "")
        if not self.api_key:
            msg = "DEEPSEEK_API_KEY environment variable is not set"
            raise ValueError(msg)

    def ask(self, query: str, context: dict, file_path: Path | None = None) -> str:
        """Send a query to DeepSeek and return the response."""
        try:
            import openai

            # DeepSeek uses OpenAI's client with a custom base URL
            client = openai.OpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com"
            )
            prompt = self._build_prompt(query, context, file_path)
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500,
            )
            return response.choices[0].message.content or "No response"
        except Exception as e:  # noqa: BLE001
            return f"DeepSeek error: {e}"
