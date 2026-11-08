"""
Day16_01 - LangGraph Basic Graph: action executor.

This helper is used alongside the agent loop (loop.py) to actually run the
tool/action chosen by the planner, by calling it on the MCP server. It
takes whatever the server returns and normalizes it into a plain string
so it's easy to store as an "observation" in the agent's state.
"""

# execute_tool() does the actual MCP call for a given tool name.
from mcp_client import execute_tool


async def execute_action(action, state, client):
    # Ask the MCP server to run the chosen tool/action.
    result = await execute_tool(
        client,
        action
    )

    # MCP results are often wrapped in a "content" object; unwrap it to get
    # the plain text the tool returned.
    if hasattr(result, "content"):

        if result.content:

            return result.content[0].text

    # Fallback: if the result doesn't look like the expected MCP shape,
    # just stringify it so callers always get text back.
    return str(result)
