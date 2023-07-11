from src.domain import UpsetThread
from src.data.redis_db import AppStateRedisDb, CharactersRedisDb
from src.integrations.startgg.api import get_characters


app_state_redis_db = AppStateRedisDb()
characters_redis_db = CharactersRedisDb()


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


def get_upset_thread(sets):

    winners, losers, notables, dqs, other = [], [], [], [], []

    for s in sets:
        if s.is_winners_bracket() and apply_filter(
                s.upset_factor,
                s.winner.initial_seed,
                s.loser.initial_seed,
                s.is_dq(),
                min_upset_factor=1,
                max_seed=50,
        ):
            winners.append(s)
        elif not s.is_winners_bracket() and apply_filter(
                s.upset_factor,
                s.winner.initial_seed,
                s.loser.initial_seed,
                s.is_dq(),
                min_upset_factor=1,
                max_seed=50
        ):
            losers.append(s)
        elif s.is_dq_and_out() and apply_filter(
                s.upset_factor,
                s.winner.initial_seed,
                s.loser.initial_seed,
                is_dq=True,
                include_dq=True,
        ):
            dqs.append(s)
        elif s.is_notable() and apply_filter(
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


def get_character_name(character_key):
    if not app_state_redis_db.is_characters_loaded():
        res = get_characters()
        characters_redis_db.add_characters(res['data']['videogame']['characters'])
        app_state_redis_db.set_is_character_loaded(1)
    return characters_redis_db.get_character_name(character_key)
