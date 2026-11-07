def check_tool(result, expected_tool):
    for message in result["messages"]:

        tool_calls = getattr(
            message,
            "tool_calls",
            []
        )

        for call in tool_calls:

            if call["name"] == expected_tool:
                return True

    return False
