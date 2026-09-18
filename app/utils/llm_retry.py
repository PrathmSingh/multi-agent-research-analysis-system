import time


def _is_quota_exhausted_error(exc: Exception) -> bool:
    """
    Detect errors caused by an exhausted daily/model quota.

    These errors should not be retried because retrying will
    not restore the available quota.
    """

    error_text = str(exc).lower()

    quota_indicators = [
        "generate_content_free_tier_requests",
        "generaterequestsperdayperprojectpermodelfreetier",
        "daily quota",
        "quota exceeded",
        "quotaexceeded",
    ]

    return any(
        indicator in error_text
        for indicator in quota_indicators
    )


def _is_retryable_error(exc: Exception) -> bool:
    """
    Determine whether an LLM error is likely temporary.
    """

    error_text = str(exc).lower()

    retryable_indicators = [
        "503",
        "unavailable",
        "service unavailable",
        "temporarily unavailable",
        "429",
        "resource_exhausted",
        "rate limit",
        "too many requests",
        "timeout",
        "timed out",
        "connection",
    ]

    return any(
        indicator in error_text
        for indicator in retryable_indicators
    )


def invoke_with_retry(
    llm,
    prompt: str,
    max_attempts: int = 3,
    base_delay: float = 2.0,
):
    """
    Invoke an LLM with retry handling for temporary failures.

    Daily quota exhaustion is detected and raised immediately
    without wasting additional retry attempts.
    """

    last_exception = None

    for attempt in range(1, max_attempts + 1):

        try:
            return llm.invoke(prompt)

        except Exception as exc:
            last_exception = exc

            # Do not retry when the daily/model quota is exhausted.
            if _is_quota_exhausted_error(exc):
                raise RuntimeError(
                    "LLM daily/model quota has been exhausted. "
                    "Please wait for the quota to reset or use "
                    "a model/provider with available quota."
                ) from exc

            # Do not retry errors that are clearly non-temporary.
            if not _is_retryable_error(exc):
                raise RuntimeError(
                    f"LLM call failed with a non-retryable error: "
                    f"{exc}"
                ) from exc

            if attempt == max_attempts:
                break

            delay = base_delay * (2 ** (attempt - 1))

            time.sleep(delay)

    raise RuntimeError(
        f"LLM call failed after {max_attempts} attempts: "
        f"{last_exception}"
    ) from last_exception


def invoke_structured_with_retry(
    llm,
    schema,
    prompt: str,
    max_attempts: int = 3,
    base_delay: float = 2.0,
):
    """
    Invoke a structured-output LLM with retry handling.

    This handles both:
    - with_structured_output() failures
    - structured LLM invocation failures

    Daily quota exhaustion is detected and raised immediately.
    """

    last_exception = None

    for attempt in range(1, max_attempts + 1):

        try:
            structured_llm = llm.with_structured_output(
                schema
            )

            return structured_llm.invoke(prompt)

        except Exception as exc:
            last_exception = exc

            # Do not retry daily/model quota exhaustion.
            if _is_quota_exhausted_error(exc):
                raise RuntimeError(
                    "LLM daily/model quota has been exhausted. "
                    "Please wait for the quota to reset or use "
                    "a model/provider with available quota."
                ) from exc

            # Do not retry clearly non-temporary errors.
            if not _is_retryable_error(exc):
                raise RuntimeError(
                    f"Structured LLM call failed with a "
                    f"non-retryable error: {exc}"
                ) from exc

            if attempt == max_attempts:
                break

            delay = base_delay * (2 ** (attempt - 1))

            time.sleep(delay)

    raise RuntimeError(
        f"Structured LLM call failed after "
        f"{max_attempts} attempts: {last_exception}"
    ) from last_exception