"""
Day 18.02 - Agent Testing (Integration) - the research agent itself.

This file wires an Ollama chat model up to two tools (search_web and
read_webpage) and runs a classic "tool calling" loop: ask the model for a
response, and if it asks to call a tool, run that tool and feed the result
back in, repeating until the model gives a final answer with no more tool
calls. test_agent.py exercises this end-to-end as an integration test.
"""

# chat() sends a message list (and optionally tool definitions) to the
# local Ollama model and gets a response back.
from ollama import chat
from tools import (
    search_web,
    read_webpage
)
# The local model to use for the agent's reasoning.
MODEL = "qwen3:4b"
# Maps tool names (as the model will refer to them) to the real Python
# functions we actually call.
AVAILABLE_TOOLS = {
    "search_web": search_web,
    "read_webpage": read_webpage
}
# The tool function list passed to Ollama so it knows what tools exist
# and how to call them (their signatures/docstrings describe usage).
TOOLS = [
    search_web,
    read_webpage
]
def research_agent(user_request):

    # Start the conversation with the user's research request.
    messages = [
        {
            "role": "user",
            "content": user_request
        }
    ]

    # Keep looping: ask the model, run any requested tools, repeat.
    while True:

        response = chat(
            model=MODEL,
            messages=messages,
            tools=TOOLS
        )

        # Record the assistant's reply (including any tool calls) in the
        # conversation history so the model has full context next turn.
        messages.append(
            response.message
        )

        # No tool call means the model is done - return its final answer.
        if not response.message.tool_calls:
            print("\nNo tool call. Returning final answer.")
            return response.message.content

        # The model may request one or more tool calls in a single turn;
        # execute each of them in order.
        for tool_call in (
            response.message.tool_calls
        ):

            tool_name = (
                tool_call.function.name
            )

            arguments = (
                tool_call.function.arguments
            )

            print(
                f"\nCalling tool: {tool_name}"
            )

            print(
                f"Arguments: {arguments}"
            )

            # Look up the real Python function for this tool name.
            tool_function = (
                AVAILABLE_TOOLS.get(
                    tool_name
                )
            )

            if tool_function is None:

                # Defensive fallback in case the model hallucinates a tool
                # name that doesn't exist.
                result = (
                    f"Unknown tool: "
                    f"{tool_name}"
                )

            else:

                # Call the real tool with the arguments the model supplied.
                result = tool_function(
                    **arguments
                )

            # Feed the tool's result back into the conversation as a
            # "tool" message so the model can use it in its next turn.
            messages.append({
                "role": "tool",
                "content": str(result),
                "tool_name": tool_name
            })
