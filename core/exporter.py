import csv
import os
from typing import List, Tuple

def export_to_csv(games: List[Tuple[int]], filename: str):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["jogo", "d1", "d2", "d3", "d4", "d5", "d6"])

        for i, game in enumerate(games, 1):
            writer.writerow([i, *game])
