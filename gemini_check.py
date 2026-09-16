from app.config.llm import llm


def test_gemini_connection():
    response = llm.invoke(
        "Explain what an AI agent is in one sentence."
    )

    assert response.content