"""
Day10_01_TaskPlanning_StructuredTasks - task_planner.py

This module implements the "goal decomposition" step that makes Day10's
agent different from Day09's plain ReAct loop: instead of deciding one
action at a time from scratch, it first asks the LLM to break the user's
overall request into an ordered list of small, concrete tasks. The agent
loop (loop.py) then works through this task list one at a time.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables (e.g. BASE_URL, API_KEY, MODEL) from .env.
load_dotenv()

# Create the AI client used to talk to the LLM provider.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def decompose_task(user_request):
    # Ask the LLM to split the user's request into an ordered, one-task-
    # per-line plan with no numbering or explanations.
    prompt = f"""
You are an AI task planner.

Break the user's request into smaller tasks.

Rules:

1. Create only necessary tasks.
2. Put tasks in execution order.
3. Each task should be a short action.
4. Return one task per line.
5. Do not number the tasks.
6. Do not explain anything.

User Request:

{user_request}
"""

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "system",
                "content": "You are an AI task planner."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content.strip()

    # Split the LLM's reply into individual, non-empty task strings.
    tasks = []

    for line in result.splitlines():

        line = line.strip()

        if line:
            tasks.append(line)

    return tasks
