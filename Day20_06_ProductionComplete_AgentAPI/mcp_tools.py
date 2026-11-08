"""
Day 20.06 - Production Complete Agent API.

Defines the MCP (Model Context Protocol) client that the agent uses to
reach tools living in a separate process (server.py). Instead of importing
those tool functions directly, the agent launches server.py as a subprocess
and talks to it over stdio, which mirrors how real-world MCP tool servers
(often written in other languages or run remotely) are integrated.
"""

from langchain_mcp_adapters.client import MultiServerMCPClient

# Configure one MCP server named "time_server" that is started by running
# `python server.py` as a stdio subprocess. LangChain communicates with it
# using the MCP protocol to discover and call its tools (current_time,
# roll_dice, generate_password).
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
