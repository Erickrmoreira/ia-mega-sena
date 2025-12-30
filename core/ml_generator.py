import pandas as pd
from core.scoring import extract_features

def generate_games_with_model(
    candidate_games,
    model,
    hot,
    warm,
    cold,
    pairs,
    repeated,
    top_n=100
):
    rows = []

    for game in candidate_games:
        features = extract_features(
            game, hot, warm, cold, pairs, repeated
        )
        rows.append({
            "game": game,
            **features
        })

    df = pd.DataFrame(rows)

    X = df.drop(columns=["game"])
    df["predicted_score"] = model.predict(X)

    df = df.sort_values(
        by="predicted_score",
        ascending=False
    )

    selected = df.head(top_n)

    return selected[["game", "predicted_score"]]
