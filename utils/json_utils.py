import json
import re

def extract_json_array(text: str):
    """
    Extracts the first JSON array found in a string.
    Raises ValueError if none found.
    """
    if not text:
        raise ValueError("Empty response from LLM")

    match = re.search(r"\[[\s\S]*\]", text)
    if not match:
        raise ValueError(f"No JSON array found in LLM response:\n{text}")

    return json.loads(match.group())

def extract_json_object(text: str):
    if not text or not text.strip():
        raise ValueError("Empty response from LLM")

    match = re.search(r"\{[\s\S]*\}", text.strip())
    if not match:
        raise ValueError(f"No JSON object found:\n{text}")

    return json.loads(match.group())

def safe_json_loads(raw, fallback: dict):
    """
    Safely parse JSON from LLM output.
    Returns fallback if parsing fails.
    """
    if not raw or not raw.strip():
        return fallback

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return fallback
