def format_game(game):
    """
    Recebe uma tupla ou lista de números
    Retorna string no formato: 02 - 07 - 21 - 24 - 42 - 47
    """
    return " - ".join(f"{int(n):02d}" for n in game)
