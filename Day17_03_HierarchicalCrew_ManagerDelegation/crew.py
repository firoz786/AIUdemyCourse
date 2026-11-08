"""
Day 17.03 - Hierarchical Crew & Manager Delegation.

Defines two crews. The main `crew` uses CrewAI's `hierarchical` process:
instead of running tasks in a fixed sequence, a separate "manager" LLM
decides how to delegate work among the researcher/coder/reviewer agents.
`memory_crew` is a second, minimal crew used to demonstrate CrewAI's
long-term memory: it asks the researcher to recall information from an
earlier task, which only works if memory persisted across crew runs.
"""

from crewai import Crew, Process

from agents import (
    researcher,
    coder,
    reviewer
)

from tasks import (
    research_task,
    coding_task,
    review_task,
    memory_task
)

from llm import manager_llm

# The hierarchical crew: a manager_llm decides task delegation instead of a
# fixed sequence, and memory=True lets it recall facts across runs. The
# embedder config tells CrewAI how to turn memories into vector embeddings
# (using a local Ollama embedding model) for later recall.
crew = Crew(
    agents=[
        researcher,
        coder,
        reviewer
    ],
    tasks=[
        research_task,
        coding_task,
        review_task
    ],
    process=Process.hierarchical,
    manager_llm=manager_llm,
    memory=True,
    embedder={
        "provider": "ollama",
        "config": {
            "model_name": "nomic-embed-text",
            "url": "http://localhost:11434/api/embeddings"
        }
    },
    verbose=True
)

# A separate, minimal crew used purely to demonstrate memory recall across
# crew runs: it shares the same memory store/embedder settings as `crew`.
memory_crew = Crew(
    agents=[researcher],
    tasks=[memory_task],
    memory=True,
    embedder={
        "provider": "ollama",
        "config": {
            "model_name": "nomic-embed-text",
            "url": "http://localhost:11434/api/embeddings"
        }
    },
    verbose=True
)