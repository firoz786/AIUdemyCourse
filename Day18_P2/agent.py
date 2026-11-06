from ollama import chat
from tools import (
    search_web,
    read_webpage
)
MODEL = "qwen3:4b"
AVAILABLE_TOOLS = {
    "search_web": search_web,
    "read_webpage": read_webpage
}
TOOLS = [
    search_web,
    read_webpage
]
def research_agent(user_request):

    messages = [
        {
            "role": "user",
            "content": user_request
        }
    ]

    while True:

        response = chat(
            model=MODEL,
            messages=messages,
            tools=TOOLS
        )

        messages.append(
            response.message
        )

        if not response.message.tool_calls:
            print("\nNo tool call. Returning final answer.")
            return response.message.content

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

            tool_function = (
                AVAILABLE_TOOLS.get(
                    tool_name
                )
            )

            if tool_function is None:

                result = (
                    f"Unknown tool: "
                    f"{tool_name}"
                )

            else:

                result = tool_function(
                    **arguments
                )

            messages.append({
                "role": "tool",
                "content": str(result),
                "tool_name": tool_name
            })
