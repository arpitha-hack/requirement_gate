from llm import call_llm

def extract_requirements(text: str) -> dict:
    prompt = f"""
You are a Senior Business Analyst.

Extract structured requirement information from the text below.

Return ONLY valid JSON in this exact structure:

{{
  "id": "FR-XX",
  "title": "Requirement title",
  "description": "Clear user story or requirement",
  "acceptance_criteria": [
    "Given ... when ... then ..."
  ],
  "nfrs": [
    "Performance: ...",
    "Security: ...",
    "Usability: ...",
    "Availability: ..."
  ]
}}

Rules:
- If any section is missing, infer it
- Acceptance criteria MUST be testable
- NFRs MUST be measurable
- No markdown
- No explanations

TEXT:
{text}
"""
    return call_llm(
        system_prompt="You extract structured requirements.",
        user_prompt=prompt
    )
