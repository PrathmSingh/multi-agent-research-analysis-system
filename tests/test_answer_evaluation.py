from app.evaluation.answer_eval import calculate_answer_coverage


def test_answer_coverage_all_topics():
    report = """
    The models differ in pricing, context window,
    and capabilities.
    """

    result = calculate_answer_coverage(
        report,
        ["pricing", "context window", "capabilities"],
    )

    assert result == 1.0


def test_answer_coverage_partial_topics():
    report = """
    The models differ in pricing and capabilities.
    """

    result = calculate_answer_coverage(
        report,
        ["pricing", "context window", "capabilities"],
    )

    assert result == 2 / 3


def test_answer_coverage_no_topics():
    report = "This report discusses unrelated information."

    result = calculate_answer_coverage(
        report,
        ["pricing", "context window"],
    )

    assert result == 0.0


def test_answer_coverage_no_required_topics():
    result = calculate_answer_coverage(
        "Any report.",
        [],
    )

    assert result == 0.0