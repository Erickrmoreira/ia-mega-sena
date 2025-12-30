import random
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from core.scoring import extract_features
from core.score_function import compute_score

def train_model(
    games,
    hot,
    warm,
    cold,
    pairs,
    repeated
):
    rows = []

    for game in games:
        features = extract_features(
            game, hot, warm, cold, pairs, repeated
        )
        score = compute_score(features)
        features["score"] = score
        rows.append(features)

    df = pd.DataFrame(rows)

    X = df.drop(columns=["score"])
    y = df["score"]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )
    model.fit(X, y)

    return model, df
