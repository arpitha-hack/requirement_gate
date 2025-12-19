REQUIRED_NFRS = ["performance", "security", "usability", "availability"]

def nfr_check(nfrs):
    covered = [nfr for nfr in REQUIRED_NFRS if any(nfr in x.lower() for x in nfrs)]
    missing = list(set(REQUIRED_NFRS) - set(covered))

    score = int((len(covered) / len(REQUIRED_NFRS)) * 25)

    return {
        "covered": covered,
        "missing": missing,
        "nfr_score": score
    }
