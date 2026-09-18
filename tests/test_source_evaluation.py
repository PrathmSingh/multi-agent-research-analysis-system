from app.evaluation.source_eval import calculate_source_utilization


def test_source_utilization_all_sources_used():
    result = calculate_source_utilization(
        total_sources=3,
        cited_sources=[1, 2, 3],
    )

    assert result == 1.0


def test_source_utilization_partial_sources_used():
    result = calculate_source_utilization(
        total_sources=5,
        cited_sources=[1, 3],
    )

    assert result == 0.4


def test_source_utilization_duplicate_citations():
    result = calculate_source_utilization(
        total_sources=5,
        cited_sources=[1, 1, 2, 2],
    )

    assert result == 0.4


def test_source_utilization_no_sources():
    result = calculate_source_utilization(
        total_sources=0,
        cited_sources=[],
    )

    assert result == 0.0