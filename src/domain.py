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

    def __init__(
            self,
            identifier,
            display_score,
            full_round_text,
            total_games,
            round_num,
            losers_placement,
            winner_id,
            entrants,
            games
    ):
        self.id = identifier
        self.display_score = display_score
        self.full_round_text = full_round_text
        self.round = round_num
        self.losers_placement = losers_placement
        self.total_games = total_games
        self.games = games
        self.winner, self.loser = self.init_slots(winner_id, entrants)
        self.upset_factor = self.init_upset_factor(self.winner, self.loser)
        self.score = self.init_score(self.games, display_score, self.winner, self.loser, total_games)

    @staticmethod
    def init_slots(winner_id, entrants):
        winner, loser = entrants
        if winner_id == loser.id:
            winner, loser = loser, winner
        return winner, loser

    @staticmethod
    def init_upset_factor(winner, loser):
        return upset_factor_table.get_upset_factor(
            winner.initial_seed,
            loser.initial_seed,
        )

    @staticmethod
    def init_score(games, display_score, winner, loser, total_games):
        if games is None:
            score = display_score
            score = score.replace(winner.name, '').replace(loser.name, '').replace(' ', '')
            if score in ['0-2', '0-3', '1-2', '1-3', '2-3']:
                score = score[::-1]
            return score
        diff = total_games - len(games)
        return f'3-{diff}'

    def is_winners_bracket(self):
        return self.round > 0

    def is_dq(self):
        return self.display_score == 'DQ'

    def is_dq_and_out(self):
        return not self.is_winners_bracket() and self.is_dq()

    def is_notable(self):
        return self.score in ['3-2', '2-1']

    def get_character_selections(self, entrant_id):
        if self.games is None:
            return ''
        s = set()
        for game in self.games:
            for selection in game.selections:
                if selection.entrant.id == entrant_id:
                    s.add(selection.character.name)

        return ', '.join(sorted(list(s)))

    def get_winner_character_selections(self):
        return self.get_character_selections(self.winner.id)

    def get_loser_character_selections(self):
        return self.get_character_selections(self.loser.id)


class Entrant:

    def __init__(self, identifier, name, initial_seed):
        self.id = identifier
        self.name = name
        self.initial_seed = initial_seed


class Game:

    def __init__(self, identifier, winner_id, selections):
        self.id = identifier
        self.winner_id = winner_id
        self.selections = selections


class Selection:

    def __init__(self, entrant, character):
        self.entrant = entrant
        self.character = character


class Character:

    def __init__(self, value, name):
        self.value = value
        self.name = name


class UpsetThread:

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __init__(self, winners, losers, notables, dqs, other):
        self.winners = winners
        self.losers = losers
        self.notables = notables
        self.dqs = dqs
        self.other = other


class UpsetThreadItem:

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __eq__(self, item):
        return all([
            self.id == item.id,
            self.winners_name == item.winners_name,
            self.winners_characters == item.winners_characters,
            self.winners_seed == item.winners_seed,
            self.score == item.score,
            self.losers_name == item.losers_name,
            self.losers_characters == item.losers_characters,
            self.is_winners_bracket == item.is_winners_bracket,
            self.losers_seed == item.losers_seed,
            self.losers_placement == item.losers_placement,
            self.upset_factor == item.upset_factor,
        ])

    def __init__(
            self,
            identifier,
            winners_name,
            winners_characters,
            winners_seed,
            score,
            losers_name,
            losers_characters,
            is_winners_bracket,
            losers_seed,
            losers_placement,
            upset_factor,
    ):
        self.id = identifier
        self.winners_name = winners_name
        self.winners_characters = winners_characters
        self.winners_seed = winners_seed
        self.score = score
        self.losers_name = losers_name
        self.losers_characters = losers_characters
        self.is_winners_bracket = is_winners_bracket
        self.losers_seed = losers_seed
        self.losers_placement = losers_placement
        self.upset_factor = upset_factor
