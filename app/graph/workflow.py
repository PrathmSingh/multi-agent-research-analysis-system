from langgraph.graph import StateGraph, START, END

from app.models.state import ResearchState

from app.agents.supervisor import supervisor_agent
from app.agents.researcher import research_agent
from app.agents.analyst import analyst_agent
from app.agents.fact_checker import fact_checker_agent
from app.agents.reporter import reporter_agent
from app.agents.citation_validator import validate_citations


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

    research, sources = research_agent(state["query"])

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
        "citation_retry_count": state["citation_retry_count"] + 1,
    }


def citation_validator_node(state: ResearchState):
    """Validate citations used in the generated report."""

    validation = validate_citations(
        state["final_report"],
        state["sources"],
    )

    return {
        "citation_validation": validation,

        # Pass validation feedback back to the Reporter
        # if another generation attempt is required.
        "citation_feedback": validation["feedback"],

        "citation_retry_count": state["citation_retry_count"],
    }


# ============================================================
# Citation Retry Router
# ============================================================

def citation_retry_router(state: ResearchState):
    """
    Decide whether the report should be accepted or regenerated.

    The workflow stops when:
    1. All citations are valid, or
    2. The retry limit has been reached.
    """

    validation = state["citation_validation"]
    retry_count = state["citation_retry_count"]

    # Citations are valid → finish the workflow.
    if validation["all_citations_valid"]:
        return "end"

    # Prevent infinite report-generation loops.
    if retry_count >= 2:
        return "end"

    # Invalid citations and retries are still available.
    return "retry"


# ============================================================
# Build LangGraph Workflow
# ============================================================

builder = StateGraph(ResearchState)


# ------------------------------------------------------------
# Register Nodes
# ------------------------------------------------------------

builder.add_node("supervisor", supervisor_node)
builder.add_node("research", research_node)
builder.add_node("analyst", analyst_node)
builder.add_node("fact_checker", fact_checker_node)
builder.add_node("reporter", reporter_node)
builder.add_node("citation_validator", citation_validator_node)


# ============================================================
# Workflow Edges
# ============================================================

# Start → Supervisor
builder.add_edge(
    START,
    "supervisor",
)


# Supervisor → Research
#
# The Supervisor chooses one of:
# quick / standard / verified
#
# All three workflows begin with research.
builder.add_conditional_edges(
    "supervisor",
    lambda state: state["route"],
    {
        "quick": "research",
        "standard": "research",
        "verified": "research",
    },
)


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
builder.add_conditional_edges(
    "research",
    lambda state: state["route"],
    {
        "quick": "reporter",
        "standard": "analyst",
        "verified": "analyst",
    },
)


# Analyst → Next Agent
#
# Standard:
#     Analyst → Reporter
#
# Verified:
#     Analyst → Fact Checker
builder.add_conditional_edges(
    "analyst",
    lambda state: state["route"],
    {
        "standard": "reporter",
        "verified": "fact_checker",
    },
)


# Fact Checker → Reporter
builder.add_edge(
    "fact_checker",
    "reporter",
)


# Reporter → Citation Validator
builder.add_edge(
    "reporter",
    "citation_validator",
)


# Citation Validator → Retry or End
#
# Valid citations:
#     Citation Validator → END
#
# Invalid citations:
#     Citation Validator → Reporter
#
# Retry limit reached:
#     Citation Validator → END
builder.add_conditional_edges(
    "citation_validator",
    citation_retry_router,
    {
        "retry": "reporter",
        "end": END,
    },
)


# ============================================================
# Compile Graph
# ============================================================

graph = builder.compile()