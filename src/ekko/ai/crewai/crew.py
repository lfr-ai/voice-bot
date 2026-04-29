"""Main CrewAI crew definition for Ekko."""

from __future__ import annotations

import logging
from pathlib import Path

from crewai import Agent, Crew, Process, Task

logger = logging.getLogger(__name__)

_CONFIG_DIR = Path(__file__).parent / "config"


def _load_yaml(filename: str) -> dict:
    """Load a YAML config file."""
    import yaml

    with (_CONFIG_DIR / filename).open() as f:
        return yaml.safe_load(f)


class EkkoCrew:
    """CrewAI crew for Ekko's multi-agent workflows.

    Agents and tasks are defined in YAML config files under ``config/``.
    """

    def __init__(self) -> None:
        self._agents_config = _load_yaml("agents.yaml")
        self._tasks_config = _load_yaml("tasks.yaml")

    def _build_agent(self, agent_key: str) -> Agent:
        cfg = self._agents_config[agent_key]
        return Agent(
            role=cfg["role"],
            goal=cfg["goal"],
            backstory=cfg["backstory"],
            verbose=False,
        )

    def voice_response_crew(self, query: str) -> Crew:
        """Build a crew for handling a voice query."""
        agent = self._build_agent("voice_assistant")
        task_cfg = self._tasks_config["respond_to_query"]
        task = Task(
            description=task_cfg["description"].format(query=query),
            expected_output=task_cfg["expected_output"],
            agent=agent,
        )
        return Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)

    def transcript_analysis_crew(self, transcript: str) -> Crew:
        """Build a crew for analyzing a conversation transcript."""
        agent = self._build_agent("transcript_analyzer")
        task_cfg = self._tasks_config["analyze_transcript"]
        task = Task(
            description=task_cfg["description"].format(transcript=transcript),
            expected_output=task_cfg["expected_output"],
            agent=agent,
        )
        return Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)
