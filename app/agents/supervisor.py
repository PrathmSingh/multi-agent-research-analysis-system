from typing import Literal

from pydantic import BaseModel, Field

from app.config.llm import llm
from app.utils.llm_retry import invoke_structured_with_retry


class SupervisorDecision(BaseModel):
    route: Literal["quick", "standard", "verified"] = Field(
        description="The workflow route to use."
    )


def supervisor_agent(query: str) -> str:
    """
    Decide which workflow should be used for the user's query.
    """

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

    decision = invoke_structured_with_retry(
        llm=llm,
        schema=SupervisorDecision,
        prompt=prompt,
    )

    return decision.route