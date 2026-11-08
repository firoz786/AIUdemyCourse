"""
Day 15 - Production Engineering & Resilience: Tool Permission Checks.

This file demonstrates the "permissions" pillar of resilient agent design:
each agent role (research, coding, review, manager) is only allowed to use a
specific, pre-approved set of tools. This limits the blast radius if an agent
misbehaves or is tricked by a prompt - e.g. the coding agent can never call
get_weather. `is_tool_allowed` is the enforcement check, and
`demonstrate_permissions` prints example allow/deny decisions for teaching.
"""

# Maps each agent role to the set of tool names it is allowed to call.
# Anything not listed here is implicitly denied.
TOOL_PERMISSIONS = {

    "research": {
        "get_weather",
        "read_file"
    },

    "coding": {
        "read_file"
    },

    "review": {
        "read_file"
    },

    "manager": {
        "get_weather",
        "read_file"
    }
}


def is_tool_allowed(
    agent_name,
    tool_name
):
    # Look up the agent's allowed tool set; default to an empty set if the
    # agent name is unknown, which safely denies everything.
    allowed_tools = (
        TOOL_PERMISSIONS.get(
            agent_name,
            set()
        )
    )

    # True only if the requested tool is in that agent's allow-list.
    return (
        tool_name in allowed_tools
    )


def demonstrate_permissions():
    # A handful of (agent, tool) pairs to show both allowed and denied cases.
    examples = [
        ("research", "read_file"),
        ("coding", "get_weather"),
        ("review", "read_file"),
        ("manager", "get_weather")
    ]

    print("\nPermission Demonstration")
    print("-" * 30)

    # Print whether each example combination is ALLOWED or DENIED.
    for agent_name, tool_name in examples:

        allowed = is_tool_allowed(
            agent_name,
            tool_name
        )

        print(
            f"{agent_name:10} -> "
            f"{tool_name:12} : "
            f"{'ALLOWED' if allowed else 'DENIED'}"
        )

