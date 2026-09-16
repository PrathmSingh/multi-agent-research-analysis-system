from app.config.llm import llm
from app.models.schemas import Source


def reporter_agent(
    query: str,
    research: str,
    analysis: str,
    fact_check: str,
    sources: list[Source],
    citation_feedback: str = "",
) -> str:
    """
    Generate the final citation-backed research report.
    """

    source_text = "\n\n".join(
        f"[Source {i + 1}]\n"
        f"Title: {source.title}\n"
        f"URL: {source.url}\n"
        f"Content: {source.content}"
        for i, source in enumerate(sources)
    )

    prompt = f"""
You are a professional research report writer.

Generate a final answer to the user's research question using
only the evidence provided below.

User question:
{query}

Research:
{research}

Analysis:
{analysis}

Fact-check:
{fact_check}

Original sources:
{source_text}

Citation validation feedback:
{citation_feedback}

Requirements:
1. Answer the user's question directly.
2. Organize the answer with clear headings.
3. Include the most important findings and comparisons.
4. Use only information supported by the provided evidence.
5. Do not introduce unsupported facts.
6. Preserve source attribution for important claims.
7. Cite important claims using [Source N], where N corresponds
   to the source number provided above.
8. Do not create or invent source numbers.
9. Clearly distinguish facts from interpretation.
10. If the evidence is insufficient, say so.
11. Keep the report concise but informative.

Return a polished, citation-backed research report.
"""

    response = llm.invoke(prompt)

    return response.content[0]["text"]