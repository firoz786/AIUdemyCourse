"""
Day 18.04 - Comprehensive Tests (Full Suite) - plain Python tools.

This is the most feature-rich tools module in the Day 18 series. Besides
search_web and read_webpage, it adds a small in-memory "research notes"
store so the agent can record findings (add_research_note), list them
(get_research_notes), check them against evidence with an LLM call
(verify_finding), mark them verified (mark_note_verified), and retrieve
only the verified ones (get_verified_research_notes). Together these
tools let the agent build a fact-checked research trail instead of just
answering from memory.
"""

# requests -> makes HTTP calls to fetch web pages.
import requests
# json -> parse the JSON-formatted verification response from the model.
import json


# BeautifulSoup -> parses HTML so we can pull out specific elements/text.
from bs4 import BeautifulSoup
# urlparse/parse_qs -> help us unwrap DuckDuckGo's redirect URLs.
from urllib.parse import urlparse, parse_qs
# chat() -> used by verify_finding() to ask the model whether evidence
# actually supports a claimed finding.
from ollama import chat

# In-memory list of research notes collected during a single run. This
# resets every time the script restarts (it is not saved to disk).
research_notes = []
# The local model used for fact verification.
MODEL = "qwen3:4b"

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
        Extracted webpage text or an error message.
    """

    # Some URLs are protocol-relative (start with "//"); add "https:" so
    # requests can use them.
    if url.startswith("//"):
        url = "https:" + url

    # Extract the real URL from
    # DuckDuckGo redirect URL
    parsed_url = urlparse(url)

    # DuckDuckGo search results link through a redirect page; the real
    # destination URL is hidden in the "uddg" query parameter.
    if "duckduckgo.com" in parsed_url.netloc:
        params = parse_qs(parsed_url.query)

        if "uddg" in params:
            url = params["uddg"][0]

    try:

        # Download the actual page content.
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        response.raise_for_status()

    except requests.exceptions.RequestException as e:

        # Unlike earlier days, failures here are returned as a structured
        # error dict instead of raising, so the agent loop can keep going
        # (e.g. the LLM can see the error and try a different source).
        return {
            "status": "error",
            "url": url,
            "error": str(e)
        }

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


def add_research_note(
    source,
    finding,
    evidence
):
    """
    Store an important research finding.
IMPORTANT:
    This tool accepts exactly three arguments:

    source:
        The URL or name of the source.

    finding:
        The specific claim or conclusion
        extracted from the source.

    evidence:
        The text or information from the source
        that supports the finding.

    Do not use title or summary.
    
    Returns:
        Confirmation message.
    """

    # Append the new note with "verified" defaulting to False; it only
    # becomes True after verify_finding() confirms the evidence supports it.
    research_notes.append({
        "source": source,
        "finding": finding,
        "evidence": evidence,
        "verified": False
    })

    return {
        "status": "stored",
        "finding": finding
    }


def get_research_notes():
    """
    Return all research notes collected so far.
    """

    # Return copies so callers can't accidentally mutate our internal list.
    return [
        note.copy()
        for note in research_notes
    ]



def mark_note_verified(
    source,
    finding
):
    """
    Mark a matching research note as verified.
    """

    # Find the note matching both source and finding text, and flip its
    # verified flag to True.
    for note in research_notes:

        if (
            note["source"] == source
            and note["finding"] == finding
        ):
            note["verified"] = True

            return {
                "status": "verified",
                "finding": finding
            }

    return {
        "status": "not_found",
        "finding": finding
    }

def verify_finding(
    source,
    finding,
    evidence
):
    """
    Check whether evidence supports a finding.
    """

    # Ask the model to judge, as structured JSON, whether the evidence
    # actually backs up the claimed finding (a simple fact-checking step).
    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an evidence verification assistant. "
                    "Determine whether the supplied evidence "
                    "supports the supplied finding. "
                    "Return JSON with exactly two fields: "
                    "supported and explanation. "
                    "supported must be true or false."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Source:\n{source}\n\n"
                    f"Finding:\n{finding}\n\n"
                    f"Evidence:\n{evidence}"
                )
            }
        ],
        format="json"
    )

    # Parse the model's JSON reply into a Python dict.
    result = json.loads(
        response.message.content
    )

    # If the model judged the finding supported, mark the matching note
    # as verified so it becomes eligible for the final report.
    if result["supported"]:

        mark_note_verified(
            source,
            finding
        )

    return result

def get_verified_research_notes():
    """
    Return only verified research notes.
    """

    # Filter down to notes whose "verified" flag was set to True.
    return [
        note.copy()
        for note in research_notes
        if note.get("verified", False)
    ]
