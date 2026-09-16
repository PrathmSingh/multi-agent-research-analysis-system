from tavily import TavilyClient

from app.config.settings import TAVILY_API_KEY


tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


def web_search(query: str):
    """
    Search the web using Tavily.
    """

    response = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=5,
    )

    return response["results"]