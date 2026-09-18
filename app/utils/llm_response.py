def extract_text(response) -> str:
    """
    Safely extract text from a LangChain LLM response.

    Raises:
        RuntimeError: If the response does not contain usable text.
    """

    try:
        content = response.content

        if not content:
            raise RuntimeError(
                "LLM returned an empty response."
            )

        if isinstance(content, str):
            text = content.strip()

        elif isinstance(content, list):
            text_parts = []

            for item in content:
                if isinstance(item, dict) and "text" in item:
                    text_parts.append(item["text"])

            text = "".join(text_parts).strip()

        else:
            raise RuntimeError(
                "LLM returned an unsupported response format."
            )

    except AttributeError as exc:
        raise RuntimeError(
            "LLM response does not contain content."
        ) from exc

    if not text:
        raise RuntimeError(
            "LLM returned no usable text."
        )

    return text