"""
Day 19.06 - MCP Integration with LangChain.

This module configures the MCP client used by the rest of the project. It
tells LangChain how to start and talk to our MCP server (server.py) so that
the tools defined there (current_time, roll_dice, generate_password) can be
discovered and used by a LangChain agent, just like locally defined tools.
"""

from langchain_mcp_adapters.client import MultiServerMCPClient  # Bridges MCP servers into LangChain-compatible tools.


# Configure one MCP server named "time_server". LangChain will launch it as a
# subprocess ("python server.py") and talk to it over stdio (stdin/stdout).
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
