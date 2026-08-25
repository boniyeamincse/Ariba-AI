"""Ollama local provider implementation."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from pathlib import Path


class OllamaProvider:
    """Ollama local LLM provider."""

    def __init__(self) -> None:
        self.host = os.getenv("ARIBA_OLLAMA_HOST", "http://localhost:11434")
        self.model = os.getenv("ARIBA_OLLAMA_MODEL", "llama3.1")

    def ask(self, query: str, context: dict, file_path: Path | None = None) -> str:
        """Send a query to Ollama and return the response."""
        try:
            prompt = self._build_prompt(query, context, file_path)
            response = requests.post(
                f"{self.host}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=120,
            )
            response.raise_for_status()
            return response.json().get("response", "No response")
        except Exception as e:  # noqa: BLE001
            return f"Ollama error: {e}"

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
