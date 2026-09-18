from unittest.mock import patch

from app.evaluation.llm_judge import (
    AnswerEvaluation,
    evaluate_answer,
)


def test_llm_judge_returns_structured_evaluation():
    mock_evaluation = AnswerEvaluation(
        relevance=0.9,
        completeness=0.8,
        factuality=0.95,
        explanation="The answer is relevant and well supported.",
    )

    with patch(
        "app.evaluation.llm_judge.llm",
        create=True,
    ) as mock_llm:

        mock_llm.with_structured_output.return_value.invoke.return_value = (
            mock_evaluation
        )

        result = evaluate_answer(
            query="Compare two AI models.",
            report="Model A is faster than Model B.",
            research="Evidence about Model A and Model B.",
        )

    assert isinstance(result, AnswerEvaluation)
    assert result.relevance == 0.9
    assert result.completeness == 0.8
    assert result.factuality == 0.95


def test_llm_judge_handles_llm_failure():
    with patch(
        "app.evaluation.llm_judge.llm",
        create=True,
    ) as mock_llm:

        mock_llm.with_structured_output.side_effect = Exception(
            "Gemini evaluation failed"
        )

        try:
            evaluate_answer(
                query="Test query",
                report="Test answer",
                research="Test evidence",
            )

            assert False, "Expected RuntimeError"

        except RuntimeError as exc:
            assert "Structured LLM call failed" in str(exc)