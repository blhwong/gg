import json


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
            self.category == item.category,
            self.completed_at == item.completed_at,
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
            completed_at,
            category,
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
        self.completed_at = completed_at
        self.category = category
