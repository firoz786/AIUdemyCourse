from crewai import Crew, Process, Memory

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


crew = Crew(agents=[
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
   
    verbose=True)
    


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