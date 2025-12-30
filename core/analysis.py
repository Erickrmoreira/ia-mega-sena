import itertools
from collections import Counter
import pandas as pd

class MegaAnalysis:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numbers = df.values.flatten()

    def frequency(self):
        return Counter(self.numbers)

    def hot_warm_cold(self):
        freq = self.frequency()
        sorted_nums = freq.most_common()
        hot = [n for n, _ in sorted_nums[:15]]
        cold = [n for n, _ in sorted_nums[-15:]]
        warm = [n for n in freq if n not in hot and n not in cold]
        return hot, warm, cold

    def repeated_between_contests(self):
        from collections import Counter
        repeated = Counter()
        rows = self.df.values
        for i in range(len(rows) - 1):
            repeated.update(set(rows[i]) & set(rows[i + 1]))
        return repeated

    def pairs_frequency(self):
        pairs = Counter()
        for row in self.df.values:
            for pair in itertools.combinations(sorted(row), 2):
                pairs[pair] += 1
        return pairs

    def sequence_frequency(self):
        sequences = Counter()
        for row in self.df.values:
            row = sorted(row)
            current = [row[0]]
            for i in range(1, len(row)):
                if row[i] == row[i - 1] + 1:
                    current.append(row[i])
                else:
                    if len(current) >= 2:
                        sequences[tuple(current)] += 1
                    current = [row[i]]
            if len(current) >= 2:
                sequences[tuple(current)] += 1
        return sequences