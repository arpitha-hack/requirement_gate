from llm import call_llm

def generate_acceptance_criteria(description: str) -> str:
    prompt = f"""
You are a Business Analyst.

Generate acceptance criteria in Given-When-Then format.

CRITICAL INSTRUCTIONS:
- Return ONLY a valid JSON array
- Do NOT include explanations
- Do NOT include markdown
- Do NOT include numbering

Example output:
[
  "Given ..., when ..., then ...",
  "Given ..., when ..., then ..."
]

Requirement:
{description}
"""
    return call_llm(
        system_prompt="You generate structured acceptance criteria.",
        user_prompt=prompt
    )
