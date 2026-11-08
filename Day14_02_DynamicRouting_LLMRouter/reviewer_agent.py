"""
Day 14.02 - Dynamic Routing with an LLM Router: Reviewer Agent
----------------------------------------------------------------
Same Reviewer Agent worker as Day 14.01: it critiques the generated code
against the original task and returns a free-form text review. Structured
JSON feedback (status + feedback) is introduced later, in Day 14.03.
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


def review(
    task,
    code
):
    # Build a prompt that tells the LLM to act as a "Reviewer Agent" and
    # critique the generated code against the original task.
    prompt = f"""
You are a Reviewer Agent.

Review the following solution.

Task:
{task}

Solution:
{code}

Check:

1. Correctness
2. Python syntax
3. Logic
4. Missing issues
5. Possible improvements

Return a concise review.
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

    # Extract and return just the generated review text from the response.
    return response.choices[0].message.content
