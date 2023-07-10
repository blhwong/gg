def create_upset_factor_table():
    offset = 0
    table = []
    for i in range(20):
        row = []
        for j in range(20):
            row.append(-j + offset)
        table.append(row)
        offset += 1

    return table


upset_factor_table = create_upset_factor_table()


def get_table_idx(seed):
    seeds = [769, 513, 385, 257, 193, 129, 97, 65, 49, 33, 25, 17, 13, 9, 7, 5, 4, 3, 2, 1]

    for i, s in enumerate(seeds):
        if seed >= s:
            return 19 - i

    return 0


def calculate_upset_factor(winner_seed, loser_seed):
    w_idx, l_idx = get_table_idx(winner_seed), get_table_idx(loser_seed)
    return upset_factor_table[w_idx][l_idx]


def calculate_upset_factors(sets):
    upset_factors = []

    for s in sets:
        winner, loser = s['slots']
        if s['winnerId'] == loser['entrant']['id']:
            winner, loser = loser, winner
        upset_factors.append({
            'display_score': s['displayScore'],
            'full_round_text': s['fullRoundText'],
            'winner': winner,
            'loser': loser,
            'upset_factor': calculate_upset_factor(winner['entrant']['initialSeedNum'], loser['entrant']['initialSeedNum'])
        })

    return upset_factors
