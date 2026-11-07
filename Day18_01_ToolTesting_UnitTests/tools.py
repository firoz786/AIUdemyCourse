import requests
from bs4 import BeautifulSoup
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

    response = requests.get(
        "https://html.duckduckgo.com/html/",
        params={"q": query},
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

    results = []

    for result in soup.select(
        ".result"
    )[:max_results]:

        title_element = result.select_one(
            ".result__title"
        )

        link_element = result.select_one(
            ".result__a"
        )

        snippet_element = result.select_one(
            ".result__snippet"
        )

        if not link_element:
            continue

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


    if url.startswith("//"):
        url = "https:" + url

    # Extract the real URL from 
    #  DuckDuckGo redirect URL
    parsed_url = urlparse(url)

    if "duckduckgo.com" in parsed_url.netloc:
        params = parse_qs(parsed_url.query)

        if "uddg" in params:
            url = params["uddg"][0]
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

    for element in soup(
        ["script", "style", "noscript"]
    ):
        element.decompose()

    text = soup.get_text(
        "\n",
        strip=True
    )

    return text[:12000]

