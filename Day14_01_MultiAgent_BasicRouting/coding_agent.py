"""
Day 14.01 - Multi-Agent Basic Routing: Coding Agent
----------------------------------------------------
This file defines the "Coding Agent", one worker in our first multi-agent
system. Its only job is to take a task description plus the notes produced
by the Research Agent and ask the LLM to turn them into working Python
code. The Manager (see manager.py) calls `write_code()` as a fixed step in
a hardcoded pipeline: research -> code -> review.
"""

# Official OpenAI SDK client - used to send chat requests to the LLM.
from openai import OpenAI
# Loads key/value pairs from a local .env file into environment variables.
from dotenv import load_dotenv
# Standard library module used to read those environment variables.
import os


# Read the .env file now so os.getenv() calls below can find BASE_URL / API_KEY / MODEL.
load_dotenv()


# Create one shared OpenAI client for this module, configured from environment
# variables so the same code can point at OpenAI or any OpenAI-compatible endpoint.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


def write_code(
    task,
    research
):
    # Build a prompt that tells the LLM to act as a "Coding Agent" and write
    # Python code using both the original task and the research findings.
    prompt = f"""
You are a Coding Agent.

Write Python code based on the task
and research.

Task:
{task}

Research:
{research}

Return:

1. Short explanation
2. Complete Python code
"""

    # Send the prompt to the LLM and get back one chat completion response.
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Extract and return just the generated text (explanation + code) from the response.
    return response.choices[0].message.content
