import json
from types import NotImplementedType


class UpsetThreadItem:

    def __repr__(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __eq__(self, other: object) -> bool | NotImplementedType:
        if not isinstance(other, UpsetThreadItem):
            return NotImplemented
        return all([
            self.id == other.id,
            self.winners_name == other.winners_name,
            self.winners_characters == other.winners_characters,
            self.winners_seed == other.winners_seed,
            self.score == other.score,
            self.losers_name == other.losers_name,
            self.losers_characters == other.losers_characters,
            self.is_winners_bracket == other.is_winners_bracket,
            self.losers_seed == other.losers_seed,
            self.losers_placement == other.losers_placement,
            self.upset_factor == other.upset_factor,
            self.category == other.category,
            self.completed_at == other.completed_at,
        ])

    def __init__(
            self,
            identifier: id,
            winners_name: str,
            winners_characters: str,
            winners_seed: int,
            score: str,
            losers_name: str,
            losers_characters: str,
            is_winners_bracket: bool,
            losers_seed: int,
            losers_placement: int,
            upset_factor: int,
            completed_at: int,
            category: str,
    ) -> None:
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


class UpsetThread:

    def __repr__(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __init__(
            self,
            winners: list[UpsetThreadItem],
            losers: list[UpsetThreadItem],
            notables: list[UpsetThreadItem],
            dqs: list[UpsetThreadItem],
            other: list[UpsetThreadItem],
    ):
        self.winners = winners
        self.losers = losers
        self.notables = notables
        self.dqs = dqs
        self.other = other
