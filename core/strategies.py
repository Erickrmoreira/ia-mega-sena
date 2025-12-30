import random

import random

def safe_sample(pool, k):
    if isinstance(pool, dict):
        pool = list(pool.keys())
    elif isinstance(pool, set):
        pool = list(pool)

    if len(pool) < k:
        pool = list(range(1, 61))

    return random.sample(pool, k)


def strategy_hot(hot, *_):
    return safe_sample(hot, 6)


def strategy_mixed(hot, warm, cold):
    game = []
    game += safe_sample(hot, 3)
    game += safe_sample(warm, 2)
    game += safe_sample(cold, 1)

    # completa se faltar número
    all_nums = list(set(hot + warm + cold))
    while len(game) < 6:
        game.append(random.choice(all_nums))

    return game[:6]


def strategy_repeated(repeated, *_):
    if not repeated:
        return random.sample(range(1, 61), 6)
    return safe_sample(repeated, 6)


import random

def strategy_pairs(pairs, *_):
    if not pairs:
        return random.sample(range(1, 61), 6)

    # pairs é dict {(a,b): freq}
    sorted_pairs = sorted(
        pairs.items(),
        key=lambda x: x[1],
        reverse=True
    )

    nums = set()

    for (a, b), _ in sorted_pairs[:3]:
        nums.add(a)
        nums.add(b)

    while len(nums) < 6:
        nums.add(random.randint(1, 60))

    return list(nums)[:6]



import random

def strategy_sequences(sequences):
    """
    sequences pode ser:
    - lista de ints
    - lista de listas
    - lista de tuplas
    - lista de ((seq), score)
    """

    flat = []

    for item in sequences:
        if isinstance(item, (list, tuple)):
            # ((1,2,3), score) ou (1,2,3)
            if len(item) > 0 and isinstance(item[0], (list, tuple)):
                flat.extend(item[0])
            else:
                flat.extend(item)
        elif isinstance(item, int):
            flat.append(item)

    flat = list(set(flat))

    if len(flat) < 6:
        flat.extend(range(1, 61))

    return random.sample(flat, 6)

def strategy_random():
    return random.sample(range(1, 61), 6)
