from typing import Literal

from pydantic import BaseModel, Field

from app.config.llm import llm


class SupervisorDecision(BaseModel):
    route: Literal["quick", "standard", "verified"] = Field(
        description="The workflow route to use."
    )


def supervisor_agent(query: str) -> str:
    """
    Decide which workflow should be used for the user's query.
    """

    structured_llm = llm.with_structured_output(SupervisorDecision)

    prompt = f"""
You are the supervisor of a multi-agent research system.

User query:
{query}

Choose exactly one workflow:

quick:
- Simple factual questions.
- Web research followed by a concise answer.
- No deep analysis or fact-checking.

standard:
- Questions requiring multiple sources, comparisons,
  summaries, or deeper analysis.
- Research followed by analysis and final reporting.

verified:
- Complex comparisons, current information,
  important factual claims, or questions where accuracy
  and source verification are especially important.
- Research followed by analysis, fact-checking, and final reporting.

Return the most appropriate workflow.
"""

    decision = structured_llm.invoke(prompt)

    return decision.route