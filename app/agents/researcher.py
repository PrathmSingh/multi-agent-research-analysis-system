from app.config.llm import llm
from app.models.schemas import Source
from app.tools.web_search import web_search
from app.utils.llm_response import extract_text
from app.utils.llm_retry import invoke_with_retry


def research_agent(query: str) -> tuple[str, list[Source]]:
    """
    Research a user query using web search and an LLM.
    Returns a research summary and structured sources.
    """

    search_results = web_search(query)

    sources = [
        Source(
            title=result["title"],
            url=result["url"],
            content=result["content"],
        )
        for result in search_results
    ]

    source_text = "\n\n".join(
        f"Title: {source.title}\n"
        f"URL: {source.url}\n"
        f"Content: {source.content}"
        for source in sources
    )

    prompt = f"""
You are a research assistant.

Research the user's question using the web search results provided below.

User question:
{query}

Web search results:
{source_text}

Your task:
1. Identify the most relevant information.
2. Use only information supported by the search results.
3. Preserve important facts and details.
4. Mention source URLs for important claims.
5. Clearly separate confirmed information from uncertainty.

Provide a concise, structured research summary.
"""

    try:
        response = invoke_with_retry(
            llm,
            prompt,
        )

    except Exception as exc:
        raise RuntimeError(
            f"Research LLM call failed: {exc}"
        ) from exc

    try:
        research = extract_text(response)

    except RuntimeError as exc:
        raise RuntimeError(
            f"Invalid research LLM response: {exc}"
    ) from exc

    return research, sources