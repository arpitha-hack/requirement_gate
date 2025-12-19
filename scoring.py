def calculate_total_score(scores):
    return sum(scores.values())

def gate_decision(score, threshold=75):
    return "PASS" if score >= threshold else "FAIL"
