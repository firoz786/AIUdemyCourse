"""
Day13_02 - Registry Agent: Dynamic Tool Discovery
===================================================
This module builds a "tool registry" that merges tools from several
MCP servers into one lookup table. This is the core registry pattern
reused from Day13_01: instead of an agent hard-coding which server owns
which tool, it connects to every server up front, records which client
offers which tool name, and can then run any tool by name without
caring which server actually implements it.
"""
from mcp_client import connect, disconnect, discover_tools, execute_tool


async def create_tool_registry(servers):
    """Connect to every server in `servers` and build a combined tool registry.

    Returns a tuple of (clients, tool_registry) where `clients` is the
    list of open connections (needed later for cleanup) and
    `tool_registry` maps each tool name to the client that can run it.
    """
    clients = []
    tool_registry = {}

    for server in servers:
        # Open a connection to this one server.
        client = await connect(server)
        clients.append(client)

        # Ask the server which tools it exposes.
        tools = await discover_tools(client)

        for tool in tools:
            # Record which client owns this tool name, so `run_tool`
            # can route calls to the right server later.
            tool_registry[tool.name] = {
                "client": client,
                "tool": tool
            }

    return clients, tool_registry


async def close_servers(clients):
    """Disconnect every open client connection."""
    for client in clients:
        await disconnect(client)


async def run_tool(tool_registry, tool_name, arguments):
    """Look up which client owns `tool_name` and execute it there."""
    entry = tool_registry.get(tool_name)

    if entry is None:
        # Fail loudly if the agent asks for a tool no server exposes.
        raise ValueError(f"Unknown tool: {tool_name}")

    return await execute_tool(entry["client"], tool_name, arguments)

