# gates/requirement_gate.py

from utils.file_parser import extract_text_from_file
from extractors.requirement_extractor import extract_requirements
from utils.json_utils import extract_json_object


def run_requirement_gate(uploaded_file):
    """
    Runs requirement quality checks and returns:
    - gate_result (dict)
    - extracted_requirements (dict)
    """

    # 1. Parse file
    raw_text = extract_text_from_file(uploaded_file)

    # 2. AI requirement extraction
    raw_ai_output = extract_requirements(raw_text)

    # 3. Convert AI output to clean JSON
    extracted_requirements = extract_json_object(raw_ai_output)

    # 4. Quality checks (simple version – extensible)
    total = len(extracted_requirements.get("requirements", []))
    ambiguous = sum(
        1 for r in extracted_requirements.get("requirements", [])
        if r.get("ambiguity", "").lower() == "high"
    )

    score = 0 if total == 0 else int(((total - ambiguous) / total) * 100)

    status = "PASS" if score >= 70 else "FAIL"

    # gate_result = {
    #     "status": status,
    #     "quality_score": score,
    #     "total_requirements": total,
    #     "ambiguous_requirements": ambiguous
    # }

    # return gate_result, extracted_requirements
    gate_result = {
        "passed": passed,
        "score": total_score,
        "details": breakdown,
        "feedback": feedback
    }

    post_gate_result = handle_post_gate_actions(gate_result, req)

    gate_result["post_gate_action"] = post_gate_result

    return gate_result

