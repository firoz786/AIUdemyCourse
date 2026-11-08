"""
Day13_03 - Registry Integration: The Complete Loop
====================================================
This is the weather MCP server for the final Day13 demo. Unlike the
time server (still run over local stdio), this server now runs as a
standalone HTTP service on 127.0.0.1:8000 so `runner.py` can connect to
it as a remote MCP server - this is the "complete loop" this folder's
name refers to: a registry that transparently mixes local and remote
tools behind one agent loop.
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
    # Run as an HTTP server (instead of the default stdio transport) so
    # it can be reached remotely at http://127.0.0.1:8000/mcp.
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000
    )
