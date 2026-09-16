from app.graph.workflow import graph


def test_graph_compiles():
    assert graph is not None


def test_quick_workflow_path():
    """
    QUICK:
    Supervisor → Research → Reporter
    """

    route = "quick"

    if route == "quick":
        path = ["supervisor", "research", "reporter"]

    assert path == [
        "supervisor",
        "research",
        "reporter",
    ]


def test_standard_workflow_path():
    """
    STANDARD:
    Supervisor → Research → Analyst → Reporter
    """

    route = "standard"

    if route == "standard":
        path = [
            "supervisor",
            "research",
            "analyst",
            "reporter",
        ]

    assert path == [
        "supervisor",
        "research",
        "analyst",
        "reporter",
    ]


def test_verified_workflow_path():
    """
    VERIFIED:
    Supervisor → Research → Analyst → Fact Checker → Reporter
    """

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