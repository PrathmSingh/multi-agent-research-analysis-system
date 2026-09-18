import os

import pytest

from app.config.llm import llm


@pytest.mark.integration
def test_gemini_connection():
    if not os.getenv("GEMINI_API_KEY"):
        pytest.skip("GEMINI_API_KEY is not configured.")

    response = llm.invoke(
        "Explain what an AI agent is in one sentence."
    )

    assert response.content
