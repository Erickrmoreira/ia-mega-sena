import random
from collections import Counter
from core.validator import valid_game


def generate_games(
    n_games,
    hot,
    warm,
    cold,
    repeated,
    pairs,
    sequences,
    strategies
):
    games = set()

    # 👉 controla quantas vezes cada número aparece no conjunto final
    usage_counter = Counter()

    # 👉 limite máximo de uso por número (25% dos jogos)
    MAX_USAGE = max(1, int(n_games * 0.25))

    max_attempts = n_games * 100  # evita loop infinito
    attempts = 0

    while len(games) < n_games and attempts < max_attempts:
        attempts += 1

        strat = random.choice(strategies)

        try:
            game = strat(hot, warm, cold, repeated, pairs, sequences)
        except Exception:
            continue

        # garante int puro + ordenação
        game = tuple(sorted(int(x) for x in game))

        if not valid_game(list(game)):
            continue

        # 👉 evita números saturados
        if any(usage_counter[n] >= MAX_USAGE for n in game):
            continue

        # 👉 evita jogos muito parecidos
        if any(len(set(game) & set(g)) >= 4 for g in games):
            continue

        # jogo aprovado
        games.add(game)
        for n in game:
            usage_counter[n] += 1

    if len(games) < n_games:
        print(f"⚠️ Aviso: apenas {len(games)} jogos gerados (limite atingido)")

    return list(games)


# ✅ FUNÇÃO RANDOM PURA (fallback / baseline)
def generate_games_random(n_games: int):
    games = set()

    while len(games) < n_games:
        game = tuple(sorted(random.sample(range(1, 61), 6)))
        if valid_game(list(game)):
            games.add(game)

    return list(games)
