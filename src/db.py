from startgg.api import get_characters
from domain import UpsetThread


class SetsInMemoryDb:

    def __init__(self):
        self.storage = {}

    def add_sets(self, sets):
        for s in sets:
            self.storage[s.id] = s

    @staticmethod
    def apply_filter(
            upset_factor,
            winner_initial_seed,
            loser_initial_seed,
            is_dq,
            min_upset_factor=-float('inf'),
            max_seed=float('inf'),
            include_dq=False,
    ):
        fulfills_min_upset_factor = upset_factor >= min_upset_factor
        fulfills_not_dq = not is_dq or include_dq
        fulfills_max_seed = any([winner_initial_seed <= max_seed, loser_initial_seed <= max_seed])
        return all([
            fulfills_min_upset_factor,
            fulfills_not_dq,
            fulfills_max_seed,
        ])

    def get_upset_thread(self):

        winners, losers, notables, dqs, other = [], [], [], [], []

        for s in self.storage.values():
            if s.is_winners_bracket() and self.apply_filter(
                    s.upset_factor,
                    s.winner.initial_seed,
                    s.loser.initial_seed,
                    s.is_dq(),
                    min_upset_factor=1,
                    max_seed=50,
            ):
                winners.append(s)
            elif not s.is_winners_bracket() and self.apply_filter(
                    s.upset_factor,
                    s.winner.initial_seed,
                    s.loser.initial_seed,
                    s.is_dq(),
                    min_upset_factor=1,
                    max_seed=50
            ):
                losers.append(s)
            elif s.is_dq_and_out() and self.apply_filter(
                    s.upset_factor,
                    s.winner.initial_seed,
                    s.loser.initial_seed,
                    is_dq=True,
                    include_dq=True,
                    min_upset_factor=-float('inf'),
                    max_seed=float('inf'),
            ):
                dqs.append(s)
            elif s.is_notable() and self.apply_filter(
                    -s.upset_factor,
                    s.winner.initial_seed,
                    s.loser.initial_seed,
                    s.is_dq(),
                    min_upset_factor=3,
                    max_seed=50,
            ):
                notables.append(s)
            else:
                other.append(s)

        return UpsetThread(
            winners,
            losers,
            sorted(notables, key=lambda x: x.upset_factor),
            dqs, other)


class CharactersInMemoryDb:

    def __init__(self):
        self.storage = {}
        res = get_characters()
        for character in res['data']['videogame']['characters']:
            self.storage[character['id']] = character['name']

    def get_character_name(self, value):
        return self.storage[value]
