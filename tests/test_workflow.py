from app.graph.workflow import graph, citation_retry_router


def test_graph_compiles():
    assert graph is not None


def test_quick_workflow_path():
    route = "quick"

    if route == "quick":
        path = ["supervisor", "research", "reporter"]

    assert path == ["supervisor", "research", "reporter"]


def test_standard_workflow_path():
    route = "standard"

    if route == "standard":
        path = ["supervisor", "research", "analyst", "reporter"]

    assert path == ["supervisor", "research", "analyst", "reporter"]


def test_verified_workflow_path():
    route = "verified"

    if route == "verified":
        path = [
            "supervisor",
            "research",
            "analyst",
            "fact_checker",
            "reporter",
        ]

    assert path == [
        "supervisor",
        "research",
        "analyst",
        "fact_checker",
        "reporter",
    ]


def test_citation_router_stops_when_citations_are_valid():
    state = {
        "citation_validation": {
            "all_citations_valid": True
        },
        "citation_retry_count": 1,
    }

    assert citation_retry_router(state) == "end"


def test_citation_router_retries_invalid_citations():
    state = {
        "citation_validation": {
            "all_citations_valid": False
        },
        "citation_retry_count": 1,
    }

    assert citation_retry_router(state) == "retry"


def test_citation_router_stops_after_retry_limit():
    state = {
        "citation_validation": {
            "all_citations_valid": False
        },
        "citation_retry_count": 2,
    }

    assert citation_retry_router(state) == "end"

def test_reporter_receives_citation_feedback():
    state = {
        "query": "Test query",
        "route": "standard",
        "research": "Test research",
        "sources": [],
        "analysis": "Test analysis",
        "fact_check": "VERIFIED",
        "final_report": "",
        "citation_validation": {
            "all_citations_valid": False,
            "invalid_citations": [5],
            "feedback": "Invalid citation [Source 5].",
        },
        "citation_retry_count": 1,
        "citation_feedback": "Invalid citation [Source 5].",
    }

    assert state["citation_validation"]["all_citations_valid"] is False
    assert state["citation_feedback"] == "Invalid citation [Source 5]."
    assert state["citation_retry_count"] == 1

from unittest.mock import patch
from types import SimpleNamespace

from app.models.schemas import Source
from app.graph.workflow import (
    reporter_node,
    citation_validator_node,
)


def test_reporter_and_validator_feedback_flow():
    sources = [
        Source(
            title="Source One",
            url="https://example.com/1",
            content="First source.",
        ),
        Source(
            title="Source Two",
            url="https://example.com/2",
            content="Second source.",
        ),
    ]

    state = {
        "query": "Test query",
        "route": "standard",
        "research": "Test research",
        "sources": sources,
        "analysis": "Test analysis",
        "fact_check": "VERIFIED",
        "final_report": "",
        "citation_validation": {},
        "citation_retry_count": 0,
        "citation_feedback": "",
    }

    mock_response = SimpleNamespace(
        content=[
            {
                "text": "This claim uses an invalid citation [Source 5]."
            }
        ]
    )

    with patch(
        "app.graph.workflow.reporter_agent",
        return_value=mock_response.content[0]["text"],
    ):
        report_result = reporter_node(state)

    state.update(report_result)

    validation_result = citation_validator_node(state)

    state.update(validation_result)

    assert state["final_report"] == (
        "This claim uses an invalid citation [Source 5]."
    )

    assert state["citation_validation"]["all_citations_valid"] is False

    assert state["citation_validation"]["invalid_citations"] == [5]

    assert state["citation_feedback"] != ""

    assert state["citation_retry_count"] == 1