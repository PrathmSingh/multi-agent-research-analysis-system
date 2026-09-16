import re

from app.models.schemas import Source


def validate_citations(
    report: str,
    sources: list[Source],
) -> dict:
    """
    Validate source references used in a generated report.
    """

    cited_numbers = [
        int(number)
        for number in re.findall(r"\[Source (\d+)\]", report)
    ]

    valid_source_numbers = set(range(1, len(sources) + 1))

    invalid_citations = [
        number
        for number in cited_numbers
        if number not in valid_source_numbers
    ]

    invalid_citations = sorted(set(invalid_citations))
    cited_numbers = sorted(set(cited_numbers))

    if invalid_citations:
        feedback = (
            f"Invalid citations detected: {invalid_citations}. "
            f"Only sources 1-{len(sources)} are available. "
            "Regenerate the report using only valid source references."
        )
    else:
        feedback = "All citation references are valid."

    return {
        "cited_sources": cited_numbers,
        "invalid_citations": invalid_citations,
        "all_citations_valid": len(invalid_citations) == 0,
        "feedback": feedback,
    }