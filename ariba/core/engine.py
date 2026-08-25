"""Core engine for processing queries and orchestrating components."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ariba.collectors.system import SystemCollector
from ariba.renderer.output import Renderer

if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class QueryContext:
    """Context for a user query."""

    query: str
    file_path: Path | None = None
    auto_approve: bool = False


class Engine:
    """Main orchestration engine."""

    def __init__(self, provider: str | None = None) -> None:
        self.provider_name = provider or os.getenv("ARIBA_AI_PROVIDER", "openai")
        self.collector = SystemCollector()
        self.renderer = Renderer()
        self._provider = None  # lazy-loaded

    def _get_provider(self):  # type: ignore[no-untyped-def]  # noqa: ANN202
        """Lazy-load the AI provider."""
        if self._provider is None:
            if self.provider_name == "openai":
                from ariba.providers.openai import OpenAIProvider

                self._provider = OpenAIProvider()
            elif self.provider_name == "gemini":
                from ariba.providers.gemini import GeminiProvider

                self._provider = GeminiProvider()
            elif self.provider_name == "claude":
                from ariba.providers.claude import ClaudeProvider

                self._provider = ClaudeProvider()
            elif self.provider_name == "ollama":
                from ariba.providers.ollama import OllamaProvider

                self._provider = OllamaProvider()
            elif self.provider_name == "deepseek":
                from ariba.providers.deepseek import DeepSeekProvider

                self._provider = DeepSeekProvider()
            else:
                msg = f"Unknown provider: {self.provider_name}"
                raise ValueError(msg)
        return self._provider

    def handle(self, query: str, file_path: Path | None = None, auto_approve: bool = False) -> str:
        """Process a user query and return a formatted response."""
        context = QueryContext(query=query, file_path=file_path, auto_approve=auto_approve)
        system_info = self.collector.collect_all()
        provider = self._get_provider()
        raw_response = provider.ask(query, system_info, file_path=file_path)
        return self.renderer.render(raw_response)
