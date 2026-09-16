from typing import TypedDict


class ResearchState(TypedDict):
    query: str
    route: str
    research: str
    analysis: str
    fact_check: str
    final_report: str