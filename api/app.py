import sys
import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware # IMPORTAÇÃO ADICIONADA
from pydantic import BaseModel
import pandas as pd

# --- TRUQUE PARA MANTER SUA ESTRUTURA ORIGINAL ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, ".."))

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

# --- CONFIGURAÇÃO DE CORS ADICIONADA ---
# Isso permite que seu dashboard na Vercel acesse a API no Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, você pode trocar "*" pelo link da Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    games: int

def format_game(game: list[int]) -> str:
    """Formata o jogo no padrão 01 - 02 - 03 - 04 - 05 - 06"""
    return " - ".join(f"{n:02d}" for n in sorted(game))

@app.post("/api/generate")
def generate_games_api(req: GenerateRequest):
    n_games = req.games
    candidates = 5000 
    
    path_virada = os.path.join(BASE_DIR, "..", "data", "mega_virada.csv")
    path_12m = os.path.join(BASE_DIR, "..", "data", "mega_12_meses.csv")

    df_virada = load_data(path_virada)
    df_12m = load_data(path_12m)
    combined = pd.concat([df_virada, df_12m], ignore_index=True)

    analysis = MegaAnalysis(combined)
    hot, warm, cold = analysis.hot_warm_cold()
    repeated = analysis.repeated_between_contests()
    pairs = analysis.pairs_frequency()

    candidate_games = generate_games_random(candidates)

    model, _ = train_model(
        candidate_games,
        hot,
        warm,
        cold,
        pairs,
        repeated
    )

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

    games_list = [list(row["game"]) for _, row in ranked_games.iterrows()]

    try:
        output_dir = os.path.join(BASE_DIR, "..", "output")
        os.makedirs(output_dir, exist_ok=True)
        ranked_games.to_csv(os.path.join(output_dir, "jogos_api.csv"), index=False)
    except:
        pass

    return {
        "total_games": len(games_list),
        "games": games_list
    }

@app.get("/api/health")
def health():
    return {"status": "ok"}