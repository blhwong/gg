import json
from src.domain import UpsetThreadItem


def redis_set_to_upset_thread_item(set_id, redis_set):
    return UpsetThreadItem(set_id, *json.loads(redis_set))


def set_to_upset_thread_item(s):
    return UpsetThreadItem(
        s.id,
        s.winner.name,
        s.get_winner_character_selections(),
        s.winner.initial_seed,
        s.score,
        s.loser.name,
        s.get_loser_character_selections(),
        s.is_winners_bracket(),
        s.loser.initial_seed,
        s.losers_placement,
        s.upset_factor,
    )
