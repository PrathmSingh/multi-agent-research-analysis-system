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
    citation_accuracy: float
    source_utilization: float
    citation_retry_count: int
    citation_feedback: str
    relevance_score: float
    completeness_score: float
    factuality_score: float
    overall_score: float