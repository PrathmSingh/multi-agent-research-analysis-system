from app.config.llm import llm


def analyst_agent(research: str) -> str:
    """
    Analyze the research collected by the Research Agent.
    """

    prompt = f"""
You are an AI analysis agent.

Analyze the research provided below.

Research:
{research}

Your task:
1. Identify the most important findings.
2. Compare relevant information.
3. Identify patterns, differences, strengths, and weaknesses.
4. Do not invent information that is not supported by the research.
5. Clearly explain your reasoning.

Provide a concise and structured analysis.
"""

    response = llm.invoke(prompt)

    return response.content[0]["text"]