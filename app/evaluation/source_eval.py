def calculate_source_utilization(
    total_sources: int,
    cited_sources: list[int],
) -> float:
    """
    Calculate the percentage of retrieved sources
    that were actually cited in the final report.
    """

    if total_sources == 0:
        return 0.0

    unique_citations = set(cited_sources)

    return len(unique_citations) / total_sources