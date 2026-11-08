"""
Day 14.05 - Parallel Agents with Concurrency: Coding Agent
----------------------------------------------------------------
Same Coding Agent worker as Day 14.04: it writes or revises Python code
using the task, research, and any reviewer feedback. This folder's "what's
new" is concurrency - see parallel_demo.py for a standalone demonstration
of running independent agent tasks in parallel with asyncio.
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
    research,
    feedback=""
):
    # Build a prompt that tells the LLM to write (or revise) Python code.
    # When `feedback` is non-empty, it is the reviewer's previous critique,
    # which nudges the LLM to fix the specific problems that were found.
    prompt = f"""
You are a Coding Agent.

Write or revise Python code based on
the task and research.

Task:
{task}

Research:
{research}

Previous Reviewer Feedback:
{feedback}

If reviewer feedback is provided,
correct the identified problems.

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

