"""
Day 11.2 - Memory Integration With Agent.

This module is the "executor" part of the agent loop: it takes the tool
name chosen by the planner and actually runs it on the MCP server, then
converts the raw MCP result into a plain string the rest of the agent
(and the user) can read.
"""

from mcp_client import execute_tool


async def execute_action(
    action,
    state,
    client
):
    """Run the tool named ``action`` via MCP and return its output as text."""

    # Call the tool on the connected MCP server (no extra arguments needed here).
    result = await execute_tool(
        client,
        action
    )

    # MCP tool results carry their payload inside a `.content` list of parts.
    if hasattr(result, "content"):

        # Use the text of the first content item, if any was returned.
        if result.content:
            return result.content[0].text

    # Fallback: if the result has no usable `.content`, stringify it directly.
    return str(result)

