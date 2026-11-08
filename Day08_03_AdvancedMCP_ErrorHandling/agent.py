"""
Day08_03_AdvancedMCP_ErrorHandling - agent.py

This file builds on Day08_02 by adding a real "plan then act then respond"
loop around the MCP tools: it asks the LLM to pick the right tool for a
user's request (the Planner), executes that tool via MCP, and then asks the
LLM again to turn the raw tool result into a natural-language answer (the
Responder). This demonstrates the core agent pattern of combining an LLM's
reasoning with real tool execution, plus basic error handling around user
input.
"""

import asyncio

from openai import OpenAI
from dotenv import load_dotenv
import os
import sys

# Load environment variables (e.g. BASE_URL, API_KEY, MODEL) from .env.
load_dotenv()

# Create the AI client used to talk to the LLM provider.
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

from mcp_client import (
    connect,
    disconnect,
    discover_tools,
    execute_tool
)


# Build Tool Descriptions
def build_tool_descriptions(tools):
    # Turn the list of MCP tool objects into one readable text block the
    # LLM can read, listing each tool's name and description.
    descriptions = ""
    for tool in tools:
        descriptions += f"""
Tool:
{tool.name}

Description:
{tool.description}
----------------------------
"""

    return descriptions


def planner(user_request, tools):
    # Build the tool list text to embed in the prompt below.
    tool_descriptions = build_tool_descriptions(
        tools
    )

    # Combine the user's request and the tool descriptions into a single
    # prompt that asks the LLM to choose exactly one tool name.
    prompt = f"""
You are an AI Planner.

Available Tools

{tool_descriptions}

Instructions

1. Select the best tool.
2. Reply ONLY with the tool name.
3. Do not explain.

User Request

{user_request}
"""
    # Send the planning prompt to the LLM.
    response = client.chat.completions.create(

        model=os.getenv("MODEL"),

        messages=[

            {
                "role": "user",
                "content": prompt
            }

        ]

    )

    # The LLM's reply is expected to be just the chosen tool's name.
    tool_name = response.choices[0].message.content

    return tool_name.strip()


def generate_response(user_request, tool_result):
    # Ask the LLM to turn the raw tool output into a friendly, natural
    # sentence instead of showing the user raw data structures.
    prompt = f"""
The user asked:

{user_request}

The tool returned:

{tool_result}

Respond directly to the user in a natural, conversational way.

Use the tool result as the factual source.
Transform raw tool output into a human-friendly answer.
Do not simply copy raw values when a natural sentence would be better.
Do not add information that is not needed to answer the request.
Do not mention tools, internal processing, planning, or reasoning.
Keep the response concise.
"""

    response = client.chat.completions.create(

        model=os.getenv("MODEL"),

        messages=[

            {
                "role": "user",
                "content": prompt
            }

        ]

    )

    return response.choices[0].message.content


async def main():
    # Step 1: Connect to the MCP Server.
    client = await connect()

    # Step 2: Discover all available tools.
    tools = await discover_tools(
        client
    )
    print()
    print("Available Tools")
    print("----------------")

    for tool in tools:
        print(tool.name)
    print()

    # Step 3: Ask the user what they want. Wrapped in try/except so that
    # Ctrl+C (KeyboardInterrupt) or an unexpected end-of-input (EOFError)
    # exits the program gracefully instead of printing a scary traceback.
    try:
        user_request = input(
            "User : "
        )
    except (KeyboardInterrupt, EOFError):
        print("\n\nInterrupted by user (Ctrl+C). Exiting gracefully...")
        sys.exit(0)

    # Step 4: Planner picks the best tool for this request.
    tool_name = planner(
        user_request,
        tools
    )

    print()

    print(
        "Planner Selected:",
        tool_name
    )

    # Step 5: Execute the selected tool via MCP.
    tool_result = await execute_tool(client, tool_name)

    # Step 6: Generate a natural language response from the raw tool result.
    final_answer = generate_response(user_request, tool_result)

    print()

    print(final_answer)

    # Step 7: Always disconnect cleanly from the MCP server.
    await disconnect(
        client
    )

if __name__ == "__main__":
    asyncio.run(main())


