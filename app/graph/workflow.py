from langgraph.graph import StateGraph, START, END

from app.models.state import ResearchState

from app.agents.supervisor import supervisor_agent
from app.agents.researcher import research_agent
from app.agents.analyst import analyst_agent
from app.agents.fact_checker import fact_checker_agent
from app.agents.reporter import reporter_agent


# -----------------------------
# Supervisor Node
# -----------------------------

def supervisor_node(state: ResearchState):
    route = supervisor_agent(state["query"])

    return {
        "route": route
    }


# -----------------------------
# Research Node
# -----------------------------

def research_node(state: ResearchState):
    research = research_agent(state["query"])

    return {
        "research": research
    }


# -----------------------------
# Analyst Node
# -----------------------------

def analyst_node(state: ResearchState):
    analysis = analyst_agent(state["research"])

    return {
        "analysis": analysis
    }


# -----------------------------
# Fact Checker Node
# -----------------------------

def fact_checker_node(state: ResearchState):
    fact_check = fact_checker_agent(
        state["research"],
        state["analysis"]
    )

    return {
        "fact_check": fact_check
    }


# -----------------------------
# Reporter Node
# -----------------------------

def reporter_node(state: ResearchState):
    final_report = reporter_agent(
        state["query"],
        state["research"],
        state["analysis"],
        state["fact_check"]
    )

    return {
        "final_report": final_report
    }


# -----------------------------
# Build LangGraph
# -----------------------------

builder = StateGraph(ResearchState)


# Add nodes
builder.add_node("supervisor", supervisor_node)
builder.add_node("research", research_node)
builder.add_node("analyst", analyst_node)
builder.add_node("fact_checker", fact_checker_node)
builder.add_node("reporter", reporter_node)


# -----------------------------
# Start → Supervisor
# -----------------------------

builder.add_edge(
    START,
    "supervisor"
)


# -----------------------------
# Supervisor → Research
# -----------------------------

builder.add_conditional_edges(
    "supervisor",
    lambda state: state["route"],
    {
        "quick": "research",
        "standard": "research",
        "verified": "research",
    }
)


# -----------------------------
# Research → Next Agent
# -----------------------------

builder.add_conditional_edges(
    "research",
    lambda state: state["route"],
    {
        "quick": "reporter",
        "standard": "analyst",
        "verified": "analyst",
    }
)


# -----------------------------
# Analyst → Next Agent
# -----------------------------

builder.add_conditional_edges(
    "analyst",
    lambda state: state["route"],
    {
        "standard": "reporter",
        "verified": "fact_checker",
    }
)


# -----------------------------
# Fact Checker → Reporter
# -----------------------------

builder.add_edge(
    "fact_checker",
    "reporter"
)


# -----------------------------
# Reporter → End
# -----------------------------

builder.add_edge(
    "reporter",
    END
)


# -----------------------------
# Compile Graph
# -----------------------------

graph = builder.compile()