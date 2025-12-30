def compute_score(features: dict) -> float:
    score = 0.0

    score += features["hot_count"] * 2
    score += features["warm_count"] * 1
    score -= features["cold_count"] * 1

    score += features["pair_score"] * 0.01
    score += features["num_sequences"] * 0.5

    if features["max_sequence_len"] > 3:
        score -= 2

    return score
