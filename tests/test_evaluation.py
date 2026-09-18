from app.evaluation.citation_eval import calculate_citation_accuracy


def test_citation_accuracy_all_valid():
    result = calculate_citation_accuracy(
        cited_sources=[1, 2, 3],
        invalid_citations=[],
    )

    assert result == 1.0


def test_citation_accuracy_with_invalid_citation():
    result = calculate_citation_accuracy(
        cited_sources=[1, 2, 5],
        invalid_citations=[5],
    )

    assert result == 2 / 3


def test_citation_accuracy_no_citations():
    result = calculate_citation_accuracy(
        cited_sources=[],
        invalid_citations=[],
    )

    assert result == 0.0