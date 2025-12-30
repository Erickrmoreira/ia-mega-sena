import argparse
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from core.loader import load_data
from core.analysis import MegaAnalysis
from core.generator import generate_games
from core.exporter import export_to_csv
from core import strategies
from core.formatter import format_game


# ===============================
# 🔹 LÓGICA CENTRAL (REUTILIZÁVEL)
# ===============================

def run_generation(n_games: int, output: str = None):
    df_virada = load_data("data/mega_virada.csv")
    df_12m = load_data("data/mega_12_meses.csv")
    combined = df_virada._append(df_12m)

    analysis = MegaAnalysis(combined)

    hot, warm, cold = analysis.hot_warm_cold()
    repeated = analysis.repeated_between_contests()
    pairs = analysis.pairs_frequency()
    sequences = analysis.sequence_frequency()

    strategy_list = [
        lambda h, w, c, r, p, s: strategies.strategy_mixed(h, w, c),
        lambda h, w, c, r, p, s: strategies.strategy_pairs(p),
        lambda h, w, c, r, p, s: strategies.strategy_sequences(s),
        lambda h, w, c, r, p, s: strategies.strategy_random(),
    ]

    games = generate_games(
        n_games=n_games,
        hot=hot,
        warm=warm,
        cold=cold,
        repeated=repeated,
        pairs=pairs,
        sequences=sequences,
        strategies=strategy_list
    )

    if output:
        export_to_csv(games, output)

    return games


# ===============================
# 🔹 CLI (continua igual)
# ===============================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Sistema inteligente de geração de apostas para Mega-Sena"
    )

    parser.add_argument("--games", type=int)
    parser.add_argument("--output", type=str, default="output/jogos_mega.csv")
    parser.add_argument("--no-print", action="store_true")

    return parser.parse_args()


def ask_games_quantity(min_q=1, max_q=100):
    while True:
        try:
            q = int(input(f"Quantos jogos você quer gerar ({min_q} a {max_q})? "))
            if min_q <= q <= max_q:
                return q
            print(f"❌ Digite um número entre {min_q} e {max_q}.")
        except ValueError:
            print("❌ Digite um número inteiro válido.")


def run_cli():
    args = parse_args()

    if args.games is not None:
        if not (1 <= args.games <= 100):
            raise ValueError("A quantidade deve estar entre 1 e 100.")
        n_games = args.games
    else:
        n_games = ask_games_quantity()

    games = run_generation(n_games, args.output)

    print(f"\n✅ {len(games)} jogos gerados")
    print(f"📄 Arquivo salvo em: {args.output}\n")

    if not args.no_print:
        for i, game in enumerate(games, start=1):
            print(f"Jogo {i:03d}: {format_game(game)}")


# ===============================
# 🔹 FASTAPI (para o React)
# ===============================

app = FastAPI(title="Mega IA")

class GenerateRequest(BaseModel):
    games: int

@app.post("/api/generate")
def generate_api(req: GenerateRequest):
    # Verifique no terminal do VS Code/Prompt se esse print aparece quando você clica no botão
    print(f"DEBUG: Recebido pedido para {req.games} jogos (Tipo: {type(req.games)})")
    
    if req.games < 1:
        return {"games": [], "error": "Quantidade inválida"}

    # Chama sua função original
    lista_de_jogos = run_generation(req.games)
    
    # IMPORTANTE: O React espera uma lista de listas para o .map funcionar
    return {
        "games": [list(g) for g in lista_de_jogos]
    }


# 🔹 Serve o dashboard React
app.mount("/", StaticFiles(directory="dashboard", html=True), name="dashboard")


# ===============================
# 🔹 ENTRYPOINT
# ===============================

if __name__ == "__main__":
    import sys

    # Se rodar: python main.py → CLI
    if len(sys.argv) > 1:
        run_cli()
    else:
        # Se rodar: python main.py (sem args) → API
        uvicorn.run(app, host="0.0.0.0", port=8000)
