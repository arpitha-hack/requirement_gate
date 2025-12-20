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

# def extract_json_object(text: str):
#     import json, re

#     match = re.search(r"\{[\s\S]*\}", text)
#     if not match:
#         raise ValueError("No JSON object found")

#     return json.loads(match.group())
def extract_json_object(text: str):
    if not text or not text.strip():
        raise ValueError("Empty response from LLM")

    match = re.search(r"\{[\s\S]*\}", text.strip())
    if not match:
        raise ValueError(f"No JSON object found:\n{text}")

    return json.loads(match.group())
