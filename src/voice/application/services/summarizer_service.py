from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from voice.config.config import Config
from voice.core.gateways.openai_gateway import OpenAIGateway


@dataclass
class SummarizerService:
    gateway: OpenAIGateway
    cfg: Config | None = None

    def summarize(self, chunks: Iterable[str]) -> str:
        """Summarize a list of text chunks into a single summary.

        Uses the OpenAI gateway to perform summarization. Keeps orchestration
        at application level (chunking, prompt assembly).
        """
        if self.cfg is None:
            cfg = Config()
        else:
            cfg = self.cfg

        prompt_path = cfg.PACKAGE_DIR_PATH / "prompts" / "summary_prompt_chunks.txt"
        system_prompt = "Summarizer"
        try:
            template = Path(prompt_path).read_text(encoding="utf-8")
        except Exception:
            template = "Summarize the following content concisely:\n{content}"

        payload = "\n\n".join(chunks)
        user_prompt = template.replace("{content}", payload)

        return self.gateway.chat(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=getattr(cfg, "DEFAULT_MODEL", "gpt-4o"),
            temperature=0.0,
            max_completion_tokens=512,
        )
