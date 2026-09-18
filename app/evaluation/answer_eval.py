def calculate_answer_coverage(
    report: str,
    required_topics: list[str],
) -> float:
    """
    Calculate how many required topics are covered
    by the generated report.

    This is a simple deterministic evaluation metric.
    It is not a semantic quality judgment.
    """

    if not required_topics:
        return 0.0

    report_lower = report.lower()

    covered_topics = sum(
        1
        for topic in required_topics
        if topic.lower() in report_lower
    )

    return covered_topics / len(required_topics)