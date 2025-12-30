from collections import Counter

def extract_features(
    game,
    hot,
    warm,
    cold,
    pairs_freq,
    repeated_freq
):
    features = {}

    features["hot_count"] = sum(1 for n in game if n in hot)
    features["warm_count"] = sum(1 for n in game if n in warm)
    features["cold_count"] = sum(1 for n in game if n in cold)

    # Sequências
    seq_len = 1
    max_seq = 1
    num_seq = 0

    game = sorted(game)
    for i in range(1, len(game)):
        if game[i] == game[i - 1] + 1:
            seq_len += 1
            max_seq = max(max_seq, seq_len)
        else:
            if seq_len >= 2:
                num_seq += 1
            seq_len = 1

    features["num_sequences"] = num_seq
    features["max_sequence_len"] = max_seq

    # Pares frequentes
    pair_score = 0
    for i in range(len(game)):
        for j in range(i + 1, len(game)):
            pair = tuple(sorted((game[i], game[j])))
            if pair in pairs_freq:
                pair_score += pairs_freq[pair]

    features["pair_score"] = pair_score

    # Repetidos
    features["repeated_score"] = sum(
        repeated_freq.get(n, 0) for n in game
    )

    return features
