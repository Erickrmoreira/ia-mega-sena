def valid_game(game: list[int]) -> bool:
    game = sorted(game)
    if len(game) != 6 or len(set(game)) != 6:
        return False
    seq = 1
    for i in range(1, 6):
        if game[i] == game[i - 1] + 1:
            seq += 1
            if seq > 3:
                return False
        else:
            seq = 1
    return True