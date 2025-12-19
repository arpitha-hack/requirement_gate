def completeness_check(req):
    missing = []

    if not req.description:
        missing.append("Description missing")
    if not req.acceptance_criteria:
        missing.append("Acceptance criteria missing")

    score = 25 if not missing else max(0, 25 - len(missing) * 10)

    return {
        "missing_items": missing,
        "completeness_score": score
    }
