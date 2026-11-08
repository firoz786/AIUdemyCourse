"""
Day09_02_ReActAgent_FullLoop - agent/executor.py

Part of the full ReAct ("Reason + Act") agent loop: this tiny module is the
"Act" step. Given an action name chosen by the planner, it calls the
matching MCP tool and extracts a plain-text observation from the tool's
result so the rest of the agent (the loop and state) can work with simple
strings instead of raw MCP response objects.
"""

from mcp_client import execute_tool


async def execute_action(action, client):
    # Ask the MCP server to run the chosen tool/action.
    result = await execute_tool(
        client,
        action
    )

    # MCP tool results carry their payload in a `content` list; pull out
    # the first item's text if present.
    if hasattr(result, "content"):

        if result.content:

            return result.content[0].text

    # Fallback: if the result doesn't have the expected shape, just
    # stringify it so the loop always gets something usable.
    return str(result)

