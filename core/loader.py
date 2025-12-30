import pandas as pd
import re

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, header=None)

    rows = []

    for _, row in df.iterrows():
        text = " ".join(map(str, row.values))
        nums = re.findall(r"\d{1,2}", text)

        # só aceita linhas com EXATAMENTE 6 números
        if len(nums) == 6:
            rows.append([int(n) for n in nums])

    if not rows:
        raise ValueError(f"Nenhuma linha válida encontrada em {path}")

    return pd.DataFrame(
        rows,
        columns=["n1", "n2", "n3", "n4", "n5", "n6"]
    )
