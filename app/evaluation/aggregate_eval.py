def calculate_overall_score(
    relevance: float,
    completeness: float,
    factuality: float,
) -> float:
    """
    Calculate the overall LLM-as-a-Judge score.

    Equal weight is currently given to all
    three evaluation dimensions.
    """

    return (
        relevance
        + completeness
        + factuality
    ) / 3