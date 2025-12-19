from llm import call_llm

def testability_check(acceptance_criteria):
    prompt = f"""
    Check whether the acceptance criteria below are testable and measurable.

    ACs:
    {acceptance_criteria}

    Respond in JSON:
    {{
      "non_testable": [],
      "testability_score": 0-25
    }}
    """

    return call_llm("You are a QA Engineer.", prompt)
