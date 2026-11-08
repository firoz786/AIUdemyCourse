"""
Day 19.09 - MCP client configuration for the capstone LangChain agent.

This module defines a shared `MultiServerMCPClient` that knows how to
start and talk to the local MCP server defined in server.py (over stdio,
i.e. by launching `python server.py` as a subprocess). Other scripts in
this folder (main.py, final_agent.py) import `client` from here to fetch
the tools that MCP server exposes (time, dice, password generator).
"""

from langchain_mcp_adapters.client import MultiServerMCPClient


# Configure one MCP server named "time_server", launched as a subprocess
# via stdio transport (the client talks to it through stdin/stdout).
client = MultiServerMCPClient(
    {
        "time_server": {
            "transport": "stdio",
            "command": "python",
            "args": [
                "server.py"
            ]
        }
    }
)
