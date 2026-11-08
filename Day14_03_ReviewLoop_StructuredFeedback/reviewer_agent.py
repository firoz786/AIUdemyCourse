"""
Day 14.03 - Review Loop with Structured Feedback: Reviewer Agent
---------------------------------------------------------------------
What's NEW in this file: instead of returning free-form review text (like
Day 14.01/14.02), the Reviewer Agent now returns STRUCTURED JSON with two
fields: "status" ("approved" or "needs_revision") and "feedback" (what to
fix). This structure is what lets the Manager programmatically decide
whether to loop back to the Coding Agent for another revision.
"""

# Official OpenAI SDK client - used to send chat requests to the LLM.
from openai import OpenAI
# Loads key/value pairs from a local .env file into environment variables.
from dotenv import load_dotenv
# Standard library module used to parse the JSON string returned by the LLM.
import json
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
    # Build a prompt that tells the LLM to act as a "Reviewer Agent" and to
    # reply with ONLY a JSON object (no prose) so it can be parsed reliably.
    prompt = f"""
You are a Reviewer Agent.

Review the following Python solution.

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

Return ONLY valid JSON.

Use exactly this format:

{{
    "status": "approved",
    "feedback": "The solution is correct."
}}

OR:

{{
    "status": "needs_revision",
    "feedback": "Explain what needs to be changed."
}}

Use "approved" only when the solution
is acceptable.

Use "needs_revision" when the solution
requires a correction.
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

    # Pull out the raw text and strip whitespace before trying to parse it.
    result = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    # Convert the JSON string into a Python dict: {"status": ..., "feedback": ...}.
    return json.loads(result)

