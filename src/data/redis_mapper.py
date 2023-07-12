import json


def from_redis_set(value):
    return json.loads(value)


def domain_to_redis_set(s):
    return json.dumps([
        s.winners_name,
        s.winners_characters,
        s.winners_seed,
        s.score,
        s.losers_name,
        s.losers_characters,
        s.is_winners_bracket,
        s.losers_seed,
        s.losers_placement,
        s.upset_factor,
    ])
