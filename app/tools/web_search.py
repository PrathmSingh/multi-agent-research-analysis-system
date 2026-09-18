from tavily import TavilyClient

from app.config.settings import TAVILY_API_KEY


# Initialize the Tavily client once.
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


def web_search(query: str):
    """
    Search the web using Tavily.

    Raises:
        ValueError: If the query is empty.
        RuntimeError: If the web search fails.
    """

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    # --------------------------------------------------------
    # Execute web search
    # --------------------------------------------------------

    try:
        response = tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
        )

    except Exception as exc:
        raise RuntimeError(
            f"Web search failed: {exc}"
        ) from exc

    # --------------------------------------------------------
    # Validate response
    # --------------------------------------------------------

    results = response.get("results", [])

    if not results:
        raise RuntimeError(
            "Web search returned no results."
        )

    return results