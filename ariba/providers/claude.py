"""Anthropic Claude provider implementation."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class ClaudeProvider:
    """Anthropic Claude API provider."""

    def __init__(self) -> None:
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if not self.api_key:
            msg = "ANTHROPIC_API_KEY environment variable is not set"
            raise ValueError(msg)

    def ask(self, query: str, context: dict, file_path: Path | None = None) -> str:
        """Send a query to Claude and return the response."""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)
            prompt = self._build_prompt(query, context, file_path)
            response = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text if response.content else "No response"
        except Exception as e:  # noqa: BLE001
            return f"Claude error: {e}"

    def _build_prompt(self, query: str, context: dict, file_path: Path | None) -> str:
        """Build the prompt for the AI model."""
        parts = [
            "You are a Linux and DevOps assistant named Ariba AI.",
            "You must natively understand and process queries in English, Bangla, and Banglish (Bengali written in English letters).",
            "Always respond in the exact same language the user used.",
            "Answer the user's question based on the system information provided.",
            "Be concise and actionable.",
            "",
            f"User question: {query}",
            "",
            "System information:",
            str(context),
        ]
        if file_path and file_path.exists():
            parts.extend(["", f"File content ({file_path}):", file_path.read_text(errors="replace")])
        return "\n".join(parts)
