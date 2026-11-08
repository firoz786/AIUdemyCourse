"""
Day 18.03 - Planner Testing (Behavior Validation) - agent and planner.

This file adds a "planner" on top of the Day 18.02 research agent: before
researching, create_research_plan() asks the model to produce an ordered,
numbered research plan from the user's request. research_agent() is the
same tool-calling loop as before. Splitting planning from execution makes
it possible to test and validate each behavior independently.
"""

# chat() sends a message list (and optionally tool definitions) to the
# local Ollama model and gets a response back.
from ollama import chat
from tools import (
    search_web,
    read_webpage
)
# The local model to use for both planning and the agent's reasoning.
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


def create_research_plan(user_request):

    # Ask the model (no tools involved) to turn the user's request into a
    # short, numbered, ordered research plan.
    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a research planning assistant. "
                    "Create a concise and ordered research plan "
                    "for the user's research request. "
                    "Return only the numbered research steps."
                )
            },
            {
                "role": "user",
                "content": user_request
            }
        ]
    )

    return response.message.content
