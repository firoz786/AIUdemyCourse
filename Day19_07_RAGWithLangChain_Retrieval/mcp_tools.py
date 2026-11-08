"""
Day 19.07 - RAG with LangChain (Retrieval).

This module configures the MCP client used by the shared agent demo
(main.py) in this folder. It tells LangChain how to start and talk to our
MCP server (server.py) so its tools can be discovered and used by a
LangChain agent, just like locally defined tools.
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
