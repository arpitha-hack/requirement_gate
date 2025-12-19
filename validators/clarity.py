from llm import call_llm

def clarity_analysis(requirement_text: str):
    prompt = f"""
    Analyze the following requirement for ambiguity and clarity.
    Identify vague terms and unclear statements.

    Requirement:
    {requirement_text}

    Respond in JSON with:
    {{
      "issues": [],
      "clarity_score": 0-25
    }}
    """

    result = call_llm("You are a Requirements Quality Analyst.", prompt)
    return result
