from schemas import RequirementInput
from validators.clarity import clarity_analysis
from validators.completeness import completeness_check
from validators.testability import testability_check
from validators.nfr import nfr_check
from generators.acceptance_criteria import generate_acceptance_criteria
from scoring import calculate_total_score, gate_decision
import json
from utils.json_utils import extract_json_array

def run_quality_gate(req_data):
    req = RequirementInput(**req_data)

    if not req.acceptance_criteria:
        raw_ac = generate_acceptance_criteria(req.description)
        req.acceptance_criteria = extract_json_array(raw_ac)


    clarity = json.loads(clarity_analysis(req.description))
    completeness = completeness_check(req)
    testability = json.loads(testability_check(req.acceptance_criteria))
    nfr = nfr_check(req.nfrs)

    scores = {
        "clarity": clarity["clarity_score"],
        "completeness": completeness["completeness_score"],
        "testability": testability["testability_score"],
        "nfr": nfr["nfr_score"]
    }

    total_score = calculate_total_score(scores)

    return {
        "requirement_id": req.id,
        "scores": scores,
        "total_score": total_score,
        "decision": gate_decision(total_score),
        "feedback": {
            "clarity_issues": clarity["issues"],
            "missing_items": completeness["missing_items"],
            "non_testable": testability["non_testable"],
            "missing_nfrs": nfr["missing"]
        }
    }

if __name__ == "__main__":
    with open("sample_inputs/user_story.json") as f:
        data = json.load(f)

    result = run_quality_gate(data)
    print(json.dumps(result, indent=2))
