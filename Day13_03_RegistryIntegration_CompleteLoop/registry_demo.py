"""
Day13_03 - Registry Integration: The Complete Loop
====================================================
This is a standalone registry smoke-test, carried over from Day13_01/02.
It connects to two independent MCP servers (time and weather), merges
their tools into one registry, prints the combined tool list, calls one
tool (`get_weather`) through the registry, and then cleanly disconnects.
The real Day13_03 upgrade (the weather server moving to a remote HTTP
transport, fully integrated with the planner loop) lives in runner.py.
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
