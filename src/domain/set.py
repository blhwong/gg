import json
from types import NotImplementedType

from logger import logging

logger = logging.getLogger(__name__)


class UpsetFactorTable:

    def __init__(self) -> None:
        offset = 0
        self.storage = []
        for i in range(20):
            row = []
            for j in range(20):
                row.append(-j + offset)
            self.storage.append(row)
            offset += 1

    @staticmethod
    def get_table_idx(seed: int) -> int:
        seeds = [769, 513, 385, 257, 193, 129, 97, 65, 49, 33, 25, 17, 13, 9, 7, 5, 4, 3, 2, 1]

        for i, s in enumerate(seeds):
            if seed >= s:
                return 19 - i

        return 0

    def get_upset_factor(self, winner_seed: int, loser_seed: int) -> int:
        w_idx, l_idx = self.get_table_idx(winner_seed), self.get_table_idx(loser_seed)
        return self.storage[w_idx][l_idx]


upset_factor_table = UpsetFactorTable()


class Entrant:

    def __repr__(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __init__(self, identifier: int, name: str, initial_seed: int, placement: int, is_final: bool) -> None:
        self.id = identifier
        self.name = name
        self.initial_seed = initial_seed
        self.placement = placement
        self.is_final = is_final

    def __eq__(self, other: object) -> bool | NotImplementedType:
        if not isinstance(other, Entrant):
            return NotImplemented
        return all([
            self.id == other.id,
            self.name == other.name,
            self.initial_seed == other.initial_seed,
            self.placement == other.placement,
            self.is_final == other.is_final,
        ])


class Character:

    def __repr__(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __init__(self, value: int, name: str) -> None:
        self.value = value
        self.name = name

    def __eq__(self, other: object) -> bool | NotImplementedType:
        if not isinstance(other, Character):
            return NotImplemented
        return all([
            self.value == other.value,
            self.name == other.name,
        ])


class Selection:

    def __repr__(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __init__(self, entrant: Entrant, character: Character) -> None:
        self.entrant = entrant
        self.character = character

    def __eq__(self, other: object) -> bool | NotImplementedType:
        if not isinstance(other, Selection):
            return NotImplemented
        return all([
            self.entrant == other.entrant,
            self.character == other.character,
        ])


class Game:

    def __repr__(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __init__(self, identifier: int, winner_id: int, selections: list[Selection]) -> None:
        self.id = identifier
        self.winner_id = winner_id
        self.selections = selections or []

    def __eq__(self, other: object) -> bool | NotImplementedType:
        if not isinstance(other, Game):
            return NotImplemented
        return all([
            self.id == other.id,
            self.winner_id == other.winner_id,
            self.selections == other.selections,
        ])


class Set:

    def __repr__(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __init__(
            self,
            identifier: int,
            display_score: str,
            full_round_text: str,
            total_games: int,
            round_num: int,
            losers_placement: int,
            winner_id: int,
            entrants: list[Entrant],
            games: list[Game],
            completed_at: int,
    ) -> None:
        self.id = identifier
        self.display_score = display_score
        self.full_round_text = full_round_text
        self.round = round_num
        self.losers_placement = losers_placement
        self.total_games = total_games
        self.games = games
        self.completed_at = completed_at
        self.winner, self.loser = self.init_slots(winner_id, entrants)
        self.upset_factor = self.init_upset_factor(self.winner.initial_seed, self.loser.initial_seed)
        self.score = self.init_score(self.games, display_score, self.winner, self.loser, total_games)

    def __eq__(self, other: object) -> bool | NotImplementedType:
        if not isinstance(other, Set):
            return NotImplemented
        return all([
            self.id == other.id,
            self.display_score == other.display_score,
            self.full_round_text == other.full_round_text,
            self.round == other.round,
            self.losers_placement == other.losers_placement,
            self.total_games == other.total_games,
            self.games == other.games,
            self.completed_at == other.completed_at,
            self.winner == other.winner,
            self.loser == other.loser,
            self.upset_factor == other.upset_factor,
            self.score == other.score,
        ])

    @staticmethod
    def init_slots(winner_id: int, entrants: list[Entrant]):
        winner, loser = entrants
        if winner_id == loser.id:
            winner, loser = loser, winner
        return winner, loser

    @staticmethod
    def init_score(
            games: list[Game],
            display_score: str,
            winner: Entrant,
            loser: Entrant,
            total_games: int,
    ) -> str | None:
        logger.debug(f'Initializing score. games={games} display_score={display_score} total_games={total_games}')
        if display_score == 'DQ':
            return 'DQ'

        if games is None:
            score = display_score
            score = score.replace(winner.name, '').replace(loser.name, '').replace(' ', '')
            if score in ['0-2', '0-3', '1-2', '1-3', '2-3']:
                score = score[::-1]
        else:
            winner_score, loser_score = 0, 0
            for game in games:
                if game.winner_id == winner.id:
                    winner_score += 1
                else:
                    loser_score += 1
            score = f'{winner_score}-{loser_score}'
        if any([
            total_games == 5 and score[0] != '3',
            total_games == 3 and score[0] != '2',
        ]):
            logger.warning(
                f'Could not init score. score={score} display_score={display_score} total_games={total_games}',
            )
            return None
        return score

    @staticmethod
    def init_upset_factor(winner_seed: int, loser_seed: int) -> int:
        return upset_factor_table.get_upset_factor(winner_seed, loser_seed)

    def is_winners_bracket(self) -> bool:
        return self.round > 0

    def is_dq(self) -> bool:
        return self.display_score == 'DQ'

    def is_dq_and_out(self) -> bool:
        return not self.is_winners_bracket() and self.is_dq()

    def is_notable(self) -> bool:
        return self.score in ['3-2', '2-1']

    def get_character_selections(self, entrant_id: int) -> str:
        if self.games is None:
            return ''
        s = set()
        for game in self.games:
            for selection in game.selections:
                if selection.entrant.id == entrant_id:
                    s.add(selection.character.name)

        return ', '.join(sorted(list(s)))

    def get_winner_character_selections(self) -> str:
        return self.get_character_selections(self.winner.id)

    def get_loser_character_selections(self) -> str:
        return self.get_character_selections(self.loser.id)
