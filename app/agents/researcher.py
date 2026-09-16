from app.config.llm import llm
from app.tools.web_search import web_search


def research_agent(query: str) -> str:
    """
    Research a user query using web search and an LLM.
    """

    search_results = web_search(query)

    sources = "\n\n".join(
        f"Title: {result['title']}\n"
        f"URL: {result['url']}\n"
        f"Content: {result['content']}"
        for result in search_results
    )

    prompt = f"""
You are a research assistant.

Research the user's question using the web search results provided below.

User question:
{query}

Web search results:
{sources}

Your task:
1. Identify the most relevant information.
2. Use only information supported by the search results.
3. Preserve important facts and details.
4. Mention the source URL for important claims.
5. Clearly separate confirmed information from uncertainty.

Provide a concise, structured research summary.
"""

    response = llm.invoke(prompt)

    return response.content[0]["text"]