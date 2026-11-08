"""
Day 18.02 - Agent Testing (Integration) - plain Python tools.

Same web research tools as Day 18.01 (search_web and read_webpage), used
here as the building blocks for an LLM-driven research agent. Keeping the
tools in their own module lets us integration-test the agent (agent.py)
and unit-test the tools (via test_tools.py) separately.
"""

# requests -> makes HTTP calls to fetch web pages.
import requests
# BeautifulSoup -> parses HTML so we can pull out specific elements/text.
from bs4 import BeautifulSoup
# urlparse/parse_qs -> help us unwrap DuckDuckGo's redirect URLs.
from urllib.parse import urlparse, parse_qs


def search_web(query, max_results=5):
    """
    Search the web using DuckDuckGo.

    Args:
        query: Search query.
        max_results: Maximum number of results.

    Returns:
        A list of search results.
    """
    # The LLM may pass max_results as a string (e.g. "3"), so coerce it to
    # an int before using it to slice the results list.
    max_results = int(max_results)
    # Call DuckDuckGo's HTML-only search endpoint (no JavaScript needed),
    # pretending to be a browser via the User-Agent header.
    response = requests.get(
        "https://html.duckduckgo.com/html/",
        params={"q": query},
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=20
    )

    # Raise an exception if the request failed (e.g. 4xx/5xx status code).
    response.raise_for_status()

    # Parse the raw HTML response into a searchable document tree.
    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    results = []

    # Each search result is wrapped in an element with the "result" class;
    # keep only up to max_results of them.
    for result in soup.select(
        ".result"
    )[:max_results]:

        # Extract the title, link, and snippet sub-elements of this result.
        title_element = result.select_one(
            ".result__title"
        )

        link_element = result.select_one(
            ".result__a"
        )

        snippet_element = result.select_one(
            ".result__snippet"
        )

        # Skip results that don't even have a link - nothing useful to return.
        if not link_element:
            continue

        # Build a simple dictionary with the text fields a caller would want,
        # falling back to an empty string if a piece is missing.
        results.append({
            "title": (
                title_element.get_text(
                    " ",
                    strip=True
                )
                if title_element
                else ""
            ),
            "url": link_element.get(
                "href",
                ""
            ),
            "snippet": (
                snippet_element.get_text(
                    " ",
                    strip=True
                )
                if snippet_element
                else ""
            )
        })

    return results


def read_webpage(url):
    """
    Download a webpage and extract its text.

    Args:
        url: Webpage URL.

    Returns:
        Extracted webpage text.
    """

    # Some URLs are protocol-relative (start with "//"); add "https:" so
    # requests can use them.
    if url.startswith("//"):
        url = "https:" + url

    # Extract the real URL from
    #  DuckDuckGo redirect URL
    parsed_url = urlparse(url)

    # DuckDuckGo search results link through a redirect page; the real
    # destination URL is hidden in the "uddg" query parameter.
    if "duckduckgo.com" in parsed_url.netloc:
        params = parse_qs(parsed_url.query)

        if "uddg" in params:
            url = params["uddg"][0]
    # Download the actual page content.
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # Remove non-visible/non-textual elements so they don't pollute the
    # extracted text (scripts, styles, and <noscript> fallbacks).
    for element in soup(
        ["script", "style", "noscript"]
    ):
        element.decompose()

    # Flatten the remaining HTML down to plain text, one line per block.
    text = soup.get_text(
        "\n",
        strip=True
    )

    # Trim to a reasonable size so it doesn't overwhelm the LLM's context.
    return text[:12000]

