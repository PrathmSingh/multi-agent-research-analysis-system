from app.config.llm import llm


def fact_checker_agent(research: str, analysis: str) -> str:
    """
    Verify the analysis against the original research.
    """

    prompt = f"""
You are a fact-checking agent.

Your task is to verify the analysis against the original research.

Original research:
{research}

Analysis:
{analysis}

Check:
1. Whether the claims in the analysis are supported by the research.
2. Whether any information was invented or exaggerated.
3. Whether important contradictions exist.
4. Whether the conclusions logically follow from the research.

For each important issue, explain what is correct or incorrect.

Finish with an overall verdict:
- VERIFIED
- PARTIALLY VERIFIED
- NOT VERIFIED

Be strict and rely only on the provided research.
"""

    response = llm.invoke(prompt)

    return response.content[0]["text"]