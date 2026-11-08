"""
Day13_01 - MCP Registry: Connecting to Multiple Servers
========================================================
This is the demo entry point for Day13_01. It shows the full registry
pattern end to end: connect to two separate MCP servers (time and
weather), merge their tools into one registry, print the combined
tool list, call one tool (`get_weather`) through the registry, and then
cleanly disconnect from both servers.
"""
import asyncio

from mcp_manager import create_tool_registry, close_servers, run_tool


async def main():
    # Paths to the two independent MCP server scripts this demo merges.
    servers = [
        "time-mcp-server/server.py",
        "weather-mcp-server/server.py"
    ]

    # Connect to both servers and build one combined tool registry.
    clients, tool_registry = await create_tool_registry(servers)

    try:
        print("\nAvailable Tools")
        print("----------------")
        # List every tool name discovered across both servers.
        for tool_name in tool_registry:
            print(tool_name)

        # Call a tool by name; the registry figures out which server
        # (client) actually implements it.
        result = await run_tool(tool_registry, "get_weather", {"city": "Delhi"})

        print("\nTool Result:")
        print(result)

    finally:
        # Always disconnect, even if something above raised an error.
        await close_servers(clients)


if __name__ == "__main__":
    asyncio.run(main())

