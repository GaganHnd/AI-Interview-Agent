from statistics import mean


def generate_summary(evaluations):

    scores = [item["score"] for item in evaluations]

    average = mean(scores)

    if average >= 8:
        recommendation = "Strong Hire"

    elif average >= 6:
        recommendation = "Hire"

    elif average >= 4:
        recommendation = "Borderline"

    else:
        recommendation = "Reject"

    strengths = []
    weaknesses = []

    for item in evaluations:
        strengths.extend(item["strengths"])
        weaknesses.extend(item["weaknesses"])

    return {
        "average_score": round(average, 2),
        "recommendation": recommendation,
        "strengths": list(set(strengths)),
        "weaknesses": list(set(weaknesses))
    }