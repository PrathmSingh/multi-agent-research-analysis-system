from typing import TypedDict

from app.models.schemas import Source


class ResearchState(TypedDict):
    query: str
    route: str
    research: str
    sources: list[Source]
    analysis: str
    fact_check: str
    final_report: str
    citation_validation: dict
    citation_retry_count: int
    citation_feedback: str