"""
Day 11.2 - Memory Integration With Agent.

This module implements the "task decomposition" step that runs before
the main agent loop: it asks an LLM to break the user's request into an
ordered list of small, concrete tasks (or no tasks at all, if the
request can be answered directly without using any tools).
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Shared OpenAI-compatible client used to decompose requests into tasks.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def decompose_task(user_request):
    """Ask the LLM to split `user_request` into an ordered task list,
    returning an empty list when no tools are needed at all."""

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

CRITICAL RULE:

Return NO tasks (or "NONE") if the user request belongs to any of the following categories:
   1. Greetings or casual conversation (e.g., "hi", "hello", "how are you?")
   2. Introductions or personal details (e.g., "my name is Pankaj", "I live in Delhi")
   3. Memory questions about past interactions (e.g., "what is my name?", "what did we discuss earlier?")
   4. General knowledge/Q&A questions that can be answered directly without tools (e.g., "what is Machine Learning?", "explain gravity")


User Request:

{user_request}
"""

    # Ask the LLM to decompose the request into a task list (or NONE).
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

    tasks = []

    # Turn the LLM's multi-line reply into a clean list of task strings.
    for line in result.splitlines():

        line = line.strip()

        if line:
            tasks.append(line)

    return tasks