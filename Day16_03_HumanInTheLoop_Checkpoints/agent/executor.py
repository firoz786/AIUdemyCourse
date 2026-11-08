"""
Day 16.03 - Human-in-the-Loop Checkpoints (LangGraph).

This small helper module is responsible for actually running the tool that
the planner chose and the human approved. It calls the tool through the MCP
client and normalizes the result into a plain string so the rest of the
agent (observations, final answer) can work with simple text.
"""

from agent.mcp_client import execute_tool


async def execute_action(action, state, client):
    """Run `action` (a tool name) via MCP and return its result as plain text."""

    # `state` is currently unused here but is kept for a consistent signature
    # with the other node functions, and in case future actions need context.
    result = await execute_tool(client, action)

    # MCP tool results are usually an object with a `.content` list of parts;
    # we only care about the first text part for this simple demo.
    if hasattr(result, "content"):
        if result.content:
            return result.content[0].text

    # Fallback: if the result doesn't look like an MCP content object,
    # just stringify it so the caller always gets text back.
    return str(result)
