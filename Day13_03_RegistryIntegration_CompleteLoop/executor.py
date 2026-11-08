"""
Day13_03 - Registry Integration: The Complete Loop
====================================================
This module is the "executor" step of the agent loop: given one action
chosen by the planner (a tool name + arguments), it looks the tool up
in the shared MCP tool registry, runs it on whichever server exposes
it - whether that server is a local script or a remote HTTP server -
and extracts a plain-text result the rest of the agent can reason
about.
"""
from mcp_manager import run_tool


async def execute_action(action, state, tool_registry):
    """Run the single action the planner chose and return its text result."""
    tool_name = action["tool"]
    arguments = action.get("arguments", {})

    # Route the call through the registry; it knows which MCP client
    # (server) actually implements this tool name.
    result = await run_tool(tool_registry, tool_name, arguments)

    # MCP tool results can carry a list of content blocks; unwrap the
    # first block's text if present, otherwise fall back to str().
    if hasattr(result, "content"):
        if result.content:
            return result.content[0].text

    return str(result)
