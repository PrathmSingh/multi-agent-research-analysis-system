from app.config.llm import llm


def reporter_agent(
    query: str,
    research: str,
    analysis: str,
    fact_check: str,
) -> str:
    """
    Generate the final research report.
    """

    prompt = f"""
You are a professional research report writer.

Generate a final answer to the user's research question using
the research, analysis, and fact-check results provided below.

User question:
{query}

Research:
{research}

Analysis:
{analysis}

Fact-check:
{fact_check}

Requirements:
1. Answer the user's question directly.
2. Organize the answer with clear headings.
3. Include the most important findings and comparisons.
4. Use only information supported by the research.
5. Do not introduce unsupported facts.
6. Preserve important source URLs from the research.
7. Clearly distinguish facts from interpretation when necessary.
8. Keep the report concise but informative.

Return a polished final research report.
"""

    response = llm.invoke(prompt)

    return response.content[0]["text"]