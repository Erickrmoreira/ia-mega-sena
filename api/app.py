from fastapi import FastAPI, Query
import pandas as pd

from core.loader import load_data
from core.analysis import MegaAnalysis
from ml.train_model import train_model
from core.ml_generator import generate_games_with_model
from core.generator import generate_games_random


app = FastAPI(
    title="Mega-Sena Intelligent Generator API",
    description="API para geração de apostas baseada em análise estatística + ML",
    version="1.0.0"
)


def format_game(game: list[int]) -> str:
    """Formata o jogo no padrão 01 - 02 - 03 - 04 - 05 - 06"""
    return " - ".join(f"{n:02d}" for n in sorted(game))


@app.get("/generate")
def generate_games_api(
    n_games: int = Query(100, gt=0, le=1000),
    candidates: int = Query(5000, gt=100, le=50000),
    save_csv: bool = True,
    output: str = "output/jogos_api.csv"
):
    # 1️⃣ Carrega dados históricos
    df_virada = load_data("data/mega_virada.csv")
    df_12m = load_data("data/mega_12_meses.csv")
    combined = pd.concat([df_virada, df_12m], ignore_index=True)

    # 2️⃣ Análise estatística
    analysis = MegaAnalysis(combined)

    hot, warm, cold = analysis.hot_warm_cold()
    repeated = analysis.repeated_between_contests()
    pairs = analysis.pairs_frequency()
    sequences = analysis.sequence_frequency()

    # 3️⃣ Gera jogos candidatos (brutos)
    candidate_games = generate_games_random(candidates)

    # 4️⃣ Treina o modelo ML com score
    model, _ = train_model(
        candidate_games,
        hot,
        warm,
        cold,
        pairs,
        repeated
    )

    # 5️⃣ Rankear jogos usando o modelo
    ranked_games = generate_games_with_model(
        candidate_games=candidate_games,
        model=model,
        hot=hot,
        warm=warm,
        cold=cold,
        pairs=pairs,
        repeated=repeated,
        top_n=n_games
    )

    # 6️⃣ Formatar saída
    ranked_games["game_formatted"] = ranked_games["game"].apply(format_game)
    ranked_games["predicted_score"] = ranked_games["predicted_score"].round(3)

    response_games = [
        {
            "game": row["game_formatted"],
            "predicted_score": row["predicted_score"]
        }
        for _, row in ranked_games.iterrows()
    ]

    # 7️⃣ Salvar CSV formatado (opcional)
    if save_csv:
        ranked_games[["game_formatted", "predicted_score"]].rename(
            columns={"game_formatted": "game"}
        ).to_csv(output, index=False)

    return {
        "total_games": len(response_games),
        "games": response_games
    }
