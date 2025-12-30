import sys
import os
from fastapi import FastAPI, Query
from pydantic import BaseModel
import pandas as pd

# --- TRUQUE PARA MANTER SUA ESTRUTURA ORIGINAL ---
# Adiciona a raiz do projeto ao caminho do Python para que ele encontre a pasta 'core' e 'ml'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, ".."))

# Agora os seus imports originais funcionam sem erro de "ModuleNotFoundError"
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

# Modelo para receber dados do app.jsx (React)
class GenerateRequest(BaseModel):
    games: int

def format_game(game: list[int]) -> str:
    """Formata o jogo no padrão 01 - 02 - 03 - 04 - 05 - 06"""
    return " - ".join(f"{n:02d}" for n in sorted(game))

# Mudamos para POST para aceitar o que o seu React envia
@app.post("/api/generate")
def generate_games_api(req: GenerateRequest):
    n_games = req.games
    candidates = 5000 
    
    # Ajuste de caminho para ler da sua pasta data original na raiz
    path_virada = os.path.join(BASE_DIR, "..", "data", "mega_virada.csv")
    path_12m = os.path.join(BASE_DIR, "..", "data", "mega_12_meses.csv")

    # 1️⃣ Carrega dados históricos
    df_virada = load_data(path_virada)
    df_12m = load_data(path_12m)
    combined = pd.concat([df_virada, df_12m], ignore_index=True)

    # 2️⃣ Análise estatística
    analysis = MegaAnalysis(combined)
    hot, warm, cold = analysis.hot_warm_cold()
    repeated = analysis.repeated_between_contests()
    pairs = analysis.pairs_frequency()

    # 3️⃣ Gera jogos candidatos (brutos)
    candidate_games = generate_games_random(candidates)

    # 4️⃣ Treina o modelo ML
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

    # 6️⃣ Formatar saída EXATAMENTE como o seu React espera
    # O React espera uma lista de listas para as bolinhas
    games_list = [list(row["game"]) for _, row in ranked_games.iterrows()]

    # 7️⃣ Salvar CSV (opcional - usando pasta temp para não dar erro na nuvem)
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

# Rota para testar se a API está viva
@app.get("/api/health")
def health():
    return {"status": "ok"}