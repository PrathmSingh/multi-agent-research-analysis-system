from app.config.llm import llm
from app.models.schemas import Source
from app.utils.llm_response import extract_text
from app.utils.llm_retry import invoke_with_retry


def analyst_agent(research: str, sources: list[Source]) -> str:
    """
    Analyze research while considering the original sources.
    """

    source_text = "\n\n".join(
        f"Title: {source.title}\n"
        f"URL: {source.url}\n"
        f"Content: {source.content}"
        for source in sources
    )

    prompt = f"""
You are an AI analysis agent.

Analyze the research provided below while cross-checking
the original sources.

Research:
{research}

Original Sources:
{source_text}

Your task:
1. Identify the most important findings.
2. Compare relevant information.
3. Identify patterns, differences, strengths, and weaknesses.
4. Cross-check important claims against the original sources.
5. Do not invent information that is not supported by the sources.
6. Clearly distinguish supported facts from interpretation.
7. Mention source URLs when relevant.

Provide a concise and structured analysis.
"""

    try:
        response = invoke_with_retry(
            llm,
            prompt,
        )

    except Exception as exc:
        raise RuntimeError(
            f"Analysis LLM call failed: {exc}"
        ) from exc

    try:
        return extract_text(response)

    except RuntimeError as exc:
        raise RuntimeError(
            f"Invalid analysis LLM response: {exc}"
        ) from exc
    