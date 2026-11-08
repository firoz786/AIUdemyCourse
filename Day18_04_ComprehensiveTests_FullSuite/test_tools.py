"""
Day 18.04 - Comprehensive Tests (Full Suite) - manual tool check.

Same manual tool smoke test as earlier days: calls search_web and
read_webpage directly to confirm the low-level web tools still work,
independent of the full agent pipeline tested in test_agent.py.
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
