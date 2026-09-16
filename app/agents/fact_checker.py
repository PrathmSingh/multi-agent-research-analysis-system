from app.config.llm import llm
from app.models.schemas import Source


def fact_checker_agent(
    research: str,
    analysis: str,
    sources: list[Source],
) -> str:
    """
    Verify the analysis against the original research and sources.
    """

    source_text = "\n\n".join(
        f"Title: {source.title}\n"
        f"URL: {source.url}\n"
        f"Content: {source.content}"
        for source in sources
    )

    prompt = f"""
You are a strict fact-checking agent.

Your task is to verify the analysis against both the
original research and the original sources.

Original research:
{research}

Original sources:
{source_text}

Analysis:
{analysis}

Check:
1. Whether important claims in the analysis are supported
   by the original sources.
2. Whether any information was invented or exaggerated.
3. Whether claims accurately represent the source content.
4. Whether important contradictions exist.
5. Whether conclusions logically follow from the evidence.
6. Whether source URLs are associated with the correct claims.

For each important issue, explain what is correct or incorrect.

Finish with an overall verdict:
- VERIFIED
- PARTIALLY VERIFIED
- NOT VERIFIED

Be strict and rely only on the provided evidence.
"""

    response = llm.invoke(prompt)

    return response.content[0]["text"]