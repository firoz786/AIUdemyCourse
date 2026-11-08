"""
Day13_02 - Registry Agent: Dynamic Tool Discovery
===================================================
This is the second of the two independent MCP servers whose tools get
merged into the registry and handed to the dynamic planner in this
folder. It exposes a single `get_weather` tool backed by a small
hard-coded lookup table, standing in for a real weather API so the
registry/planner code can focus on the MCP and agent-loop plumbing.
"""
from fastmcp import FastMCP

# Create the MCP server instance; the name shows up when clients connect.
mcp = FastMCP("Weather Server")


@mcp.tool()
def get_weather(city: str):
    """
    Return weather information for a city.
    """
    # A tiny hard-coded "database" standing in for a real weather API.
    weather_data = {
        "Delhi": "Sunny, 32°C",
        "Paris": "Cloudy, 9°C",
        "Sydney": "Rainy, 29°C",
        "London": "Partly cloudy, 15°C"
    }

    # Fall back to a friendly message for cities we don't have data for.
    return weather_data.get(city, "Weather data not available.")


if __name__ == "__main__":
    print("Starting Weather MCP Server...")
    # Run the server; FastMCP handles the stdio/transport loop.
    mcp.run()
