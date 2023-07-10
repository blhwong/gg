import json


class UpsetFactorTable:

    def __init__(self):
        offset = 0
        self.storage = []
        for i in range(20):
            row = []
            for j in range(20):
                row.append(-j + offset)
            self.storage.append(row)
            offset += 1

    @staticmethod
    def get_table_idx(seed):
        seeds = [769, 513, 385, 257, 193, 129, 97, 65, 49, 33, 25, 17, 13, 9, 7, 5, 4, 3, 2, 1]

        for i, s in enumerate(seeds):
            if seed >= s:
                return 19 - i

        return 0

    def get_upset_factor(self, winner_seed, loser_seed):
        w_idx, l_idx = self.get_table_idx(winner_seed), self.get_table_idx(loser_seed)
        return self.storage[w_idx][l_idx]


upset_factor_table = UpsetFactorTable()


class Set:

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __init__(
            self,
            display_score,
            full_round_text,
            total_games,
            winner_id,
            entrants
    ):
        self.winner = None
        self.loser = None
        self.upset_factor = 0
        self.display_score = display_score
        self.full_round_text = full_round_text
        self.total_games = total_games
        self.init_slots(winner_id, entrants)
        self.init_upset_factor()

    def init_slots(self, winner_id, entrants):
        self.winner, self.loser = entrants
        if winner_id == self.loser.id:
            self.winner, self.loser = self.loser, self.winner

    def init_upset_factor(self):
        self.upset_factor = upset_factor_table.get_upset_factor(
            self.winner.initial_seed_number,
            self.loser.initial_seed_number,
        )


class Entrant:

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __init__(self, identifier, name, initial_seed_number):
        self.id = identifier
        self.name = name
        self.initial_seed_number = initial_seed_number
