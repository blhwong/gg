import json

from src.domain.set import Set
from src.domain.upset_thread import UpsetThreadItem


def redis_set_to_upset_thread_item(set_id: str, redis_set: str) -> UpsetThreadItem:
    return UpsetThreadItem(set_id, *json.loads(redis_set))


def set_to_upset_thread_item(s: Set, category: str) -> UpsetThreadItem:
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
        s.completed_at,
        category,
    )
