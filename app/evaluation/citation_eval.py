def calculate_citation_accuracy(
    cited_sources: list[int],
    invalid_citations: list[int],
) -> float:
    """
    Calculate citation accuracy for a generated report.

    Citation accuracy measures the percentage of cited
    source references that are valid.
    """

    total_citations = len(cited_sources)

    if total_citations == 0:
        return 0.0

    valid_citations = total_citations - len(invalid_citations)

    return valid_citations / total_citations