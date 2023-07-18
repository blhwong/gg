import json

from src.domain.upset_thread import UpsetThreadItem


def from_redis_set(value: str) -> dict[str, str]:
    return json.loads(value)


def upset_thread_item_to_redis_set(item: UpsetThreadItem) -> str:
    return json.dumps([
        item.winners_name,
        item.winners_characters,
        item.winners_seed,
        item.score,
        item.losers_name,
        item.losers_characters,
        item.is_winners_bracket,
        item.losers_seed,
        item.losers_placement,
        item.upset_factor,
        item.completed_at,
        item.category,
    ])
