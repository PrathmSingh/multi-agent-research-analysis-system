from app.evaluation.aggregate_eval import calculate_overall_score


def test_calculate_overall_score():
    score = calculate_overall_score(
        relevance=0.9,
        completeness=0.8,
        factuality=1.0,
    )

    assert score == 0.9


def test_calculate_overall_score_with_zero():
    score = calculate_overall_score(
        relevance=0.0,
        completeness=0.0,
        factuality=0.0,
    )

    assert score == 0.0