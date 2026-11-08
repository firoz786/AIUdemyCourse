"""
Day 20.06 - Production Complete Agent API (evaluation).

Small evaluation helper used by run_evaluation.py to check whether the
agent actually called the tool we expected it to call for a given test
question (a basic form of automated agent testing/tool-selection grading).
"""


def check_tool(result, expected_tool):
    """Return True if expected_tool was called anywhere in the agent run."""

    # The agent's result contains a list of messages; some of those
    # messages (from the model) may include tool_calls it requested.
    for message in result["messages"]:
        tool_calls = getattr(
            message,
            "tool_calls",
            []
        )

        # Check each tool call's name against the expected tool.
        for call in tool_calls:
            if call["name"] == expected_tool:
                return True

    return False
