"""
Day 15 - Production Engineering & Resilience: Research Worker Agent.

This file demonstrates another single-purpose worker agent: given a task, it
asks the LLM (through the resilient, retrying call_llm wrapper) to gather
concepts, facts, and examples useful for the coding agent that follows it.
Note it no longer talks to the OpenAI client directly (that logic now lives
centrally in llm.py), which keeps resilience concerns like retries, timeouts,
and config in one place instead of duplicated across every worker.
"""

from llm import call_llm


def research(task):
    # Build a prompt asking the LLM to research the given task concisely.
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

    # Delegate to the shared, retrying LLM caller.
    response = call_llm(
                messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response
