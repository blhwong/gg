from src.data.redis_mapper import domain_to_redis_set, from_redis_set
from src.domain import UpsetThreadItem


s = UpsetThreadItem(
    60482457,
    'Zomba',
    'R.O.B.',
    20,
    '3-0',
    'LG | Tweek',
    'Diddy Kong, Sephiroth',
    False,
    3,
    9,
    6,
)
redis_set = domain_to_redis_set(s)
split = from_redis_set(redis_set)


def test_from_redis_set_1():
    assert split == [
        'Zomba',
        'R.O.B.',
        20,
        '3-0',
        'LG | Tweek',
        'Diddy Kong, Sephiroth',
        False,
        3,
        9,
        6,
    ]
