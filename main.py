from schemas import RequirementInput
from validators.clarity import clarity_analysis
from validators.completeness import completeness_check
from validators.testability import testability_check
from validators.nfr import nfr_check
from generators.acceptance_criteria import generate_acceptance_criteria
from scoring import calculate_total_score, gate_decision
from utils.json_utils import extract_json_array
from post_gate_actions import handle_post_gate_actions
from utils.json_utils import safe_json_loads
import json


def run_quality_gate(req_data):
    # 1. Parse input into schema
    req = RequirementInput(**req_data)

    # 2. Generate acceptance criteria if missing
    if not req.acceptance_criteria:
        raw_ac = generate_acceptance_criteria(req.description)
        req.acceptance_criteria = extract_json_array(raw_ac)

    # 3. Run validations
    clarity = json.loads(clarity_analysis(req.description))
    completeness = completeness_check(req)

    raw_testability = testability_check(req.acceptance_criteria)

    testability = safe_json_loads(
        raw_testability,
        fallback={
            "testability_score": 0,
            "non_testable": ["Testability analysis failed or returned invalid JSON"]
        }
    )
    nfr = nfr_check(req.nfrs)

    # 4. Calculate scores
    scores = {
        "clarity": clarity["clarity_score"],
        "completeness": completeness["completeness_score"],
        "testability": testability["testability_score"],
        "nfr": nfr["nfr_score"]
    }

    total_score = calculate_total_score(scores)
    decision = gate_decision(total_score)

    gate_result = {
        "passed": decision == "PASS",
        "total_score": total_score,
        "decision": decision
    }

    # 5. 🔑 POST-GATE ACTION (Azure DevOps)
    post_gate_result = handle_post_gate_actions(
        gate_result=gate_result,
        requirement=req.dict()  # convert RequirementInput → dict
    )

    # 6. Final response
    return {
        "requirement_id": req.id,
        "scores": scores,
        "total_score": total_score,
        "decision": decision,
        "feedback": {
            "clarity_issues": clarity["issues"],
            "missing_items": completeness["missing_items"],
            "non_testable": testability["non_testable"],
            "missing_nfrs": nfr["missing"]
        },
        "post_gate_action": post_gate_result
    }


if __name__ == "__main__":
    with open("sample_inputs/user_story.json") as f:
        data = json.load(f)

    result = run_quality_gate(data)
    print(json.dumps(result, indent=2))
    