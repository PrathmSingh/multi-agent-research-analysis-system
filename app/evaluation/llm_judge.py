from pydantic import BaseModel, Field

from app.config.llm import llm
from app.utils.llm_retry import invoke_structured_with_retry


class AnswerEvaluation(BaseModel):
    """
    Structured evaluation produced by the LLM judge.
    """

    relevance: float = Field(
        ge=0.0,
        le=1.0,
        description="How directly the answer addresses the user's question.",
    )

    completeness: float = Field(
        ge=0.0,
        le=1.0,
        description="How completely the answer covers the important aspects of the question.",
    )

    factuality: float = Field(
        ge=0.0,
        le=1.0,
        description="How well the answer is supported by the provided evidence.",
    )

    explanation: str = Field(
        description="Brief explanation supporting the evaluation.",
    )


def evaluate_answer(
    query: str,
    report: str,
    research: str,
) -> AnswerEvaluation:
    """
    Evaluate the final report using an LLM judge.
    """

    prompt = f"""
You are an evaluation judge for an AI research system.

Evaluate the final answer using ONLY the provided
user question and research evidence.

User question:
{query}

Research evidence:
{research}

Final answer:
{report}

Evaluate the answer on three dimensions.

1. Relevance
- Does the answer directly address the user's question?
- Penalize irrelevant information.

2. Completeness
- Does the answer cover the important aspects required
  to answer the question?
- Penalize significant omissions.

3. Factuality
- Are the claims supported by the provided research evidence?
- Penalize unsupported or contradictory claims.
- Do not assume outside knowledge.

Scoring:
0.0 = Very poor
0.5 = Partially satisfactory
1.0 = Excellent

Return scores between 0.0 and 1.0.
Provide a brief explanation for the scores.
"""

    return invoke_structured_with_retry(
        llm=llm,
        schema=AnswerEvaluation,
        prompt=prompt,
    )