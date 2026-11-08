"""
Day10_01_TaskPlanning_StructuredTasks - executor.py

This is the "Act" step for the structured task-planning agent: given a
tool name chosen by the planner for the current task, it calls that MCP
tool and extracts a plain-text observation from the result so the rest of
the loop/state can work with simple strings.
"""

from mcp_client import execute_tool


async def execute_action(
    action,
    state,
    client
):
    # Ask the MCP server to run the chosen tool for the current task.
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

