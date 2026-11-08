"""
Day 14.02 - Dynamic Routing with an LLM Router: Research Agent
--------------------------------------------------------------
Same Research Agent worker as Day 14.01: it asks the LLM to gather
concepts, facts, and examples relevant to the user's task. The Manager
now decides dynamically (via an LLM router) when to call this worker,
instead of always calling it first.
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


def research(task):
    # Build a prompt that tells the LLM to act as a "Research Agent" and
    # produce background info the other agents can rely on.
    prompt = f"""
You are a Research Agent.

Your job is to research the following task.

Task:
{task}

Provide:

1. Important concepts
2. Key facts
3. Relevant examples

Keep the response concise and useful
for another AI agent.
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

    # Extract and return just the generated research text from the response.
    return response.choices[0].message.content
