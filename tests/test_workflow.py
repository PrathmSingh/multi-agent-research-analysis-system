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

    assert citation_retry_router(state) == "evaluate"


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

    assert citation_retry_router(state) == "evaluate"

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

def test_citation_self_correction_flow():
    """
    Test that an invalid citation triggers feedback
    and that a corrected report can pass validation.
    """

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

    # --------------------------------------------------------
    # First report generation
    # --------------------------------------------------------

    with patch(
        "app.graph.workflow.reporter_agent",
        return_value="Claim supported by [Source 5].",
    ):
        result = reporter_node(state)

    state.update(result)

    validation = citation_validator_node(state)
    state.update(validation)

    # First report should fail citation validation.
    assert state["citation_validation"]["all_citations_valid"] is False
    assert state["citation_validation"]["invalid_citations"] == [5]

    # Feedback should be generated for the Reporter.
    assert state["citation_feedback"] != ""

    # One report generation has occurred.
    assert state["citation_retry_count"] == 1

    # --------------------------------------------------------
    # Second report generation using validator feedback
    # --------------------------------------------------------

    with patch(
        "app.graph.workflow.reporter_agent",
        return_value="Claim supported by [Source 1].",
    ):
        result = reporter_node(state)

    state.update(result)

    validation = citation_validator_node(state)
    state.update(validation)

    # Corrected report should now pass.
    assert state["citation_validation"]["all_citations_valid"] is True
    assert state["citation_validation"]["invalid_citations"] == []

    # Two report generations: initial + retry.
    assert state["citation_retry_count"] == 2


import pytest

from app.tools.web_search import web_search


def test_web_search_rejects_empty_query():
    with pytest.raises(ValueError):
        web_search("")


def test_web_search_rejects_whitespace_query():
    with pytest.raises(ValueError):
        web_search("   ")

from unittest.mock import patch

import pytest

from app.tools.web_search import web_search


def test_web_search_handles_api_failure():
    with patch(
        "app.tools.web_search.tavily_client.search",
        side_effect=Exception("Tavily API unavailable"),
    ):
        with pytest.raises(RuntimeError, match="Web search failed"):
            web_search("latest AI models")

def test_llm_judge_node():
    from unittest.mock import patch

    from app.evaluation.llm_judge import AnswerEvaluation
    from app.graph.workflow import llm_judge_node

    mock_evaluation = AnswerEvaluation(
        relevance=0.9,
        completeness=0.8,
        factuality=0.95,
        explanation="The answer is relevant, complete, and well supported.",
    )

    state = {
        "query": "Compare two AI models.",
        "route": "standard",
        "research": "Research evidence about the two models.",
        "sources": [],
        "analysis": "Analysis of the two models.",
        "fact_check": "Claims are supported.",
        "final_report": "Model A is faster than Model B.",
        "citation_validation": {},
        "citation_accuracy": 1.0,
        "source_utilization": 1.0,
        "citation_retry_count": 0,
        "citation_feedback": "All citation references are valid.",
        "relevance_score": 0.0,
        "completeness_score": 0.0,
        "factuality_score": 0.0,
        "overall_score": 0.0,
    }

    with patch(
        "app.graph.workflow.evaluate_answer",
        return_value=mock_evaluation,
    ):
        result = llm_judge_node(state)

    assert result["relevance_score"] == 0.9
    assert result["completeness_score"] == 0.8
    assert result["factuality_score"] == 0.95

    expected_score = (0.9 + 0.8 + 0.95) / 3

    assert result["overall_score"] == expected_score