"""
Day13_01 - MCP Registry: Connecting to Multiple Servers
========================================================
This file is the thin "client" layer used to talk to any single MCP
(Model Context Protocol) server. MCP lets an AI agent discover and call
tools exposed by separate server processes (here: a time server and a
weather server). This module wraps the low-level FastMCP `Client` so
the rest of the code can connect, list available tools, run a tool, and
disconnect without worrying about FastMCP's async context-manager API.
"""
from pathlib import Path

from fastmcp import Client


async def connect(server):
    """Open a connection to one MCP server process/script or URL."""
    # fastmcp auto-detects the right transport from the target: a local
    # script path uses stdio, while an http(s) URL uses streamable HTTP.
    # Only wrap local script paths in Path() (to avoid FastMCP's
    # deprecation warning for bare string paths) - an HTTP URL must stay
    # a plain string, since Path() would mangle its "//" into "/".
    if server.startswith("http://") or server.startswith("https://"):
        client = Client(server)
    else:
        client = Client(Path(server))

    # Manually enter the client's async context manager so the
    # connection stays open across multiple calls, instead of only
    # inside a single `async with` block.
    await client.__aenter__()

    print(f"Connected to: {server}")
    return client


async def disconnect(client):
    """Close a previously opened MCP client connection."""
    # Manually exit the async context manager to cleanly shut down
    # the connection (mirrors the __aenter__ call in connect()).
    await client.__aexit__(None, None, None)


async def discover_tools(client):
    """Ask the connected server which tools it exposes."""
    return await client.list_tools()


async def execute_tool(client, tool_name, arguments=None):
    """Call a named tool on the connected server with the given arguments."""
    if arguments is None:
        arguments = {}

    return await client.call_tool(tool_name, arguments)

