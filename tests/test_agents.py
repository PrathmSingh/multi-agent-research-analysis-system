from unittest.mock import patch
from types import SimpleNamespace
import pytest

from app.agents.researcher import research_agent
from app.models.schemas import Source


def test_research_agent_handles_llm_failure():
    mock_results = [
        {
            "title": "Test Source",
            "url": "https://example.com",
            "content": "Test research content.",
        }
    ]

    with patch(
        "app.agents.researcher.web_search",
        return_value=mock_results,
    ), patch(
        "app.agents.researcher.llm",
        create=True,
    ) as mock_llm:

        mock_llm.invoke.side_effect = Exception(
            "Gemini API unavailable"
        )

        with pytest.raises(
            RuntimeError,
            match="Research LLM call failed",
        ):
            research_agent("latest AI models")

def test_research_agent_handles_empty_llm_response():
    mock_results = [
        {
            "title": "Test Source",
            "url": "https://example.com",
            "content": "Test research content.",
        }
    ]

    mock_response = SimpleNamespace(
        content=[]
    )

    with patch(
        "app.agents.researcher.web_search",
        return_value=mock_results,
    ), patch(
        "app.agents.researcher.llm",
        create=True,
    ) as mock_llm:

        mock_llm.invoke.return_value = mock_response

        with pytest.raises(
            RuntimeError,
            match="Invalid research LLM response",
        ):
            research_agent("latest AI models")

def test_research_agent_handles_malformed_llm_response():
    mock_results = [
        {
            "title": "Test Source",
            "url": "https://example.com",
            "content": "Test research content.",
        }
    ]

    mock_response = SimpleNamespace(
        content=[{"unexpected": "value"}]
    )

    with patch(
        "app.agents.researcher.web_search",
        return_value=mock_results,
    ), patch(
        "app.agents.researcher.llm",
        create=True,
    ) as mock_llm:

        mock_llm.invoke.return_value = mock_response

        with pytest.raises(
            RuntimeError,
            match="Invalid research LLM response",
        ):
            research_agent("latest AI models")