"""
Day16_02 - Conditional Edges / Dynamic Routing (LangGraph).

This module is used by the "tool" node in graph.py. It takes the action
name the planner chose and runs it through the MCP client, then unwraps
the MCP result into a plain string observation that gets stored in the
agent's state for the planner to read on its next loop iteration.
"""

from agent.mcp_client import execute_tool


async def execute_action(action, state, client):
    # `state` isn't used here yet, but it's accepted so this function's
    # signature matches what the tool node in graph.py expects to call.
    result = await execute_tool(
        client,
        action
    )

    # MCP tool results are usually objects with a `.content` list; grab the
    # first content item's text if present.
    if hasattr(result, "content"):

        if result.content:

            return result.content[0].text

    # Fallback: if the result doesn't look like the expected MCP shape,
    # just stringify it so the planner always gets readable text back.
    return str(result)
