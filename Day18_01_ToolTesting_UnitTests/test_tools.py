"""
Day 18.01 - Tool Testing (Unit Tests) - manual smoke test script.

This is a small, manual "run it and look at the output" script (not an
automated pytest suite) that exercises the two tools defined in tools.py:
it performs a real web search, prints the results, then downloads and
prints the text of the first result's webpage. Use it to sanity-check
that the tools still work against the live DuckDuckGo site.
"""

# Import the two tool functions we want to manually verify.
from tools import (
    search_web,
    read_webpage
)

# Run a real web search for a sample query, limited to 3 results.
results = search_web(
    "AI agents software development",
    max_results=3
)

print("\nSEARCH RESULTS\n")

# Print each result's title, URL, and snippet so we can eyeball the output.
for result in results:
    print(result["title"])
    print(result["url"])
    print(result["snippet"])
    print()


if results:

    # Download and read the first search result's webpage text.
    text = read_webpage(
        results[0]["url"]
    )

    # Only print the first 2000 characters to keep the console readable.
    print("\nWEBPAGE TEXT\n")
    print(text[:2000])
