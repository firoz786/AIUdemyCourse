from crewai import Crew, Process

from agents import (
    researcher,
    coder,
    reviewer
)

from tasks import (
    research_task,
    coding_task,
    review_task
)

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
    process=Process.sequential,
    verbose=True
)


