from langgraph.graph import StateGraph, START, END

from app.models.state import ResearchState

from app.agents.supervisor import supervisor_agent
from app.agents.researcher import research_agent
from app.agents.analyst import analyst_agent
from app.agents.fact_checker import fact_checker_agent
from app.agents.reporter import reporter_agent
from app.agents.citation_validator import validate_citations

from app.evaluation.citation_eval import calculate_citation_accuracy
from app.evaluation.source_eval import calculate_source_utilization
from app.evaluation.llm_judge import evaluate_answer
from app.evaluation.aggregate_eval import calculate_overall_score


# ============================================================
# LangGraph Node Functions
# ============================================================

def supervisor_node(state: ResearchState):
    """Decide which research workflow should be executed."""

    route = supervisor_agent(state["query"])

    return {
        "route": route
    }


def research_node(state: ResearchState):
    """Search the web and collect structured research sources."""

    research, sources = research_agent(
        state["query"]
    )

    return {
        "research": research,
        "sources": sources,
    }


def analyst_node(state: ResearchState):
    """Analyze the research while considering the original sources."""

    analysis = analyst_agent(
        state["research"],
        state["sources"],
    )

    return {
        "analysis": analysis
    }


def fact_checker_node(state: ResearchState):
    """Verify the analysis against the original research and sources."""

    fact_check = fact_checker_agent(
        state["research"],
        state["analysis"],
        state["sources"],
    )

    return {
        "fact_check": fact_check
    }


def reporter_node(state: ResearchState):
    """Generate the final citation-backed research report."""

    final_report = reporter_agent(
        state["query"],
        state["research"],
        state["analysis"],
        state["fact_check"],
        state["sources"],
        state["citation_feedback"],
    )

    return {
        "final_report": final_report,

        # Track how many times the report has been generated.
        "citation_retry_count": (
            state["citation_retry_count"] + 1
        ),
    }


def citation_validator_node(state: ResearchState):
    """Validate citations and calculate citation metrics."""

    validation = validate_citations(
        state["final_report"],
        state["sources"],
    )

    citation_accuracy = calculate_citation_accuracy(
        validation["cited_sources"],
        validation["invalid_citations"],
    )

    source_utilization = calculate_source_utilization(
        total_sources=len(state["sources"]),
        cited_sources=validation["cited_sources"],
    )

    return {
        "citation_validation": validation,
        "citation_accuracy": citation_accuracy,
        "source_utilization": source_utilization,
        "citation_feedback": validation["feedback"],
        "citation_retry_count": state["citation_retry_count"],
    }


def llm_judge_node(state: ResearchState):
    """Evaluate the final report using an LLM judge."""

    evaluation = evaluate_answer(
        query=state["query"],
        report=state["final_report"],
        research=state["research"],
    )

    overall_score = calculate_overall_score(
        relevance=evaluation.relevance,
        completeness=evaluation.completeness,
        factuality=evaluation.factuality,
    )

    return {
        "relevance_score": evaluation.relevance,
        "completeness_score": evaluation.completeness,
        "factuality_score": evaluation.factuality,
        "overall_score": overall_score,
    }


# ============================================================
# Citation Retry Router
# ============================================================

def citation_retry_router(state: ResearchState):
    """
    Decide whether the report should be regenerated
    or sent to the LLM judge.

    The workflow evaluates the report when:
    1. All citations are valid, or
    2. The retry limit has been reached.
    """

    validation = state["citation_validation"]
    retry_count = state["citation_retry_count"]

    # Citations are valid → evaluate the report.
    if validation["all_citations_valid"]:
        return "evaluate"

    # Prevent infinite report-generation loops.
    if retry_count >= 2:
        return "evaluate"

    # Invalid citations and retry is still available.
    return "retry"


# ============================================================
# Build LangGraph Workflow
# ============================================================

builder = StateGraph(ResearchState)


# ============================================================
# Register Nodes
# ============================================================

builder.add_node(
    "supervisor",
    supervisor_node,
)

builder.add_node(
    "research",
    research_node,
)

builder.add_node(
    "analyst",
    analyst_node,
)

builder.add_node(
    "fact_checker",
    fact_checker_node,
)

builder.add_node(
    "reporter",
    reporter_node,
)

builder.add_node(
    "citation_validator",
    citation_validator_node,
)

builder.add_node(
    "llm_judge",
    llm_judge_node,
)


# ============================================================
# Workflow Edges
# ============================================================

# ------------------------------------------------------------
# START → Supervisor
# ------------------------------------------------------------

builder.add_edge(
    START,
    "supervisor",
)


# ------------------------------------------------------------
# Supervisor → Research
#
# Every workflow starts with research.
# ------------------------------------------------------------

builder.add_edge(
    "supervisor",
    "research",
)


# ------------------------------------------------------------
# Research → Next Agent
#
# Quick:
#     Research → Reporter
#
# Standard:
#     Research → Analyst
#
# Verified:
#     Research → Analyst
# ------------------------------------------------------------

builder.add_conditional_edges(
    "research",
    lambda state: state["route"],
    {
        "quick": "reporter",
        "standard": "analyst",
        "verified": "analyst",
    },
)


# ------------------------------------------------------------
# Analyst → Next Agent
#
# Standard:
#     Analyst → Reporter
#
# Verified:
#     Analyst → Fact Checker
# ------------------------------------------------------------

builder.add_conditional_edges(
    "analyst",
    lambda state: state["route"],
    {
        "standard": "reporter",
        "verified": "fact_checker",
    },
)


# ------------------------------------------------------------
# Fact Checker → Reporter
# ------------------------------------------------------------

builder.add_edge(
    "fact_checker",
    "reporter",
)


# ------------------------------------------------------------
# Reporter → Citation Validator
# ------------------------------------------------------------

builder.add_edge(
    "reporter",
    "citation_validator",
)


# ------------------------------------------------------------
# Citation Validator → Retry or LLM Judge
#
# Valid citations:
#     Citation Validator → LLM Judge
#
# Invalid citations:
#     Citation Validator → Reporter
#
# Retry limit reached:
#     Citation Validator → LLM Judge
# ------------------------------------------------------------

builder.add_conditional_edges(
    "citation_validator",
    citation_retry_router,
    {
        "retry": "reporter",
        "evaluate": "llm_judge",
    },
)


# ------------------------------------------------------------
# LLM Judge → END
# ------------------------------------------------------------

builder.add_edge(
    "llm_judge",
    END,
)


# ============================================================
# Compile Graph
# ============================================================

graph = builder.compile()