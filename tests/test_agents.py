from unittest.mock import patch
from types import SimpleNamespace

from app.agents.researcher import research_agent
from app.models.schemas import Source


def test_research_agent_returns_structured_sources():
    mock_results = [
        {
            "title": "Test Source",
            "url": "https://example.com",
            "content": "This is test research content.",
        }
    ]

    mock_response = SimpleNamespace(
        content=[{"text": "Test research summary."}]
    )

    with patch(
        "app.agents.researcher.web_search",
        return_value=mock_results,
    ), patch(
        "app.agents.researcher.llm",
        create=True,
    ) as mock_llm:

        mock_llm.invoke.return_value = mock_response

        research, sources = research_agent("Test query")

    assert research == "Test research summary."
    assert len(sources) == 1
    assert isinstance(sources[0], Source)
    assert sources[0].title == "Test Source"
    assert sources[0].url == "https://example.com"
    assert sources[0].content == "This is test research content."
from app.agents.citation_validator import validate_citations


def test_citation_validator():
    sources = [
        Source(
            title="Source One",
            url="https://example.com/1",
            content="First source.",
        ),
        Source(
            title="Source Two",
            url="https://example.com/2",
            content="Second source.",
        ),
    ]

    report = """
    This claim is supported [Source 1].
    Another claim is supported [Source 2].
    """

    result = validate_citations(report, sources)

    assert result["cited_sources"] == [1, 2]
    assert result["invalid_citations"] == []
    assert result["all_citations_valid"] is True
def test_citation_validator_detects_invalid_citations():
    sources = [
        Source(
            title="Source One",
            url="https://example.com/1",
            content="First source.",
        ),
        Source(
            title="Source Two",
            url="https://example.com/2",
            content="Second source.",
        ),
    ]

    report = """
    This claim is supported [Source 1].
    This citation does not exist [Source 5].
    """

    result = validate_citations(report, sources)

    assert result["cited_sources"] == [1, 5]
    assert result["invalid_citations"] == [5]
    assert result["all_citations_valid"] is False