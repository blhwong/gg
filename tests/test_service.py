import pytest
from src.data.redis_db import EventsRedisDb
from src.domain import Set, Entrant, Selection, Character
from unittest.mock import Mock, patch
from src.service import get_upset_thread, submit_to_subreddit, add_sets, get_upset_thread_redis
from src.mapper.upset_thread_mapper import set_to_upset_thread_item

e1 = Entrant(12394650, 'LG | Tweek', 3)
e2 = Entrant(12687800, 'Zomba', 20)
s1 = [Selection(e1, Character(1279, 'Diddy Kong')), Selection(e2, Character(1323, 'R.O.B.'))]
s2 = [Selection(e1, Character(1777, 'Sephiroth')), Selection(e2, Character(1323, 'R.O.B.'))]

e3 = Entrant(12394650, 'Rando 1', 100)
e4 = Entrant(12687800, 'Rando 2', 200)
s3 = [Selection(e1, Character(1279, 'Diddy Kong')), Selection(e2, Character(1323, 'R.O.B.'))]
s4 = [Selection(e1, Character(1777, 'Sephiroth')), Selection(e2, Character(1323, 'R.O.B.'))]


@pytest.fixture
def mock_events_redis_db(mocker):
    mock = Mock()
#     mocker.patch('get_upset_thread_redis.sets', return_value=mock)
    return mock


def test_get_upset_thread_1():
    winners_set = Set(
        60482457,
        'Zomba 3 - LG | Tweek 0',
        None,
        3,
        6,
        9,
        12687800,
        [e1, e2],
        None,
    )
    losers_set = Set(
        60482457,
        'Zomba 3 - LG | Tweek 0',
        None,
        3,
        -6,
        9,
        12687800,
        [e1, e2],
        None,
    )
    notables_set = Set(
        60482457,
        'LG | Tweek 3 - Zomba 2',
        None,
        3,
        6,
        9,
        12394650,
        [e1, e2],
        None,
    )
    dqs_set = Set(
        60482457,
        'DQ',
        None,
        3,
        -6,
        9,
        12687800,
        [e1, e2],
        None,
    )
    others_set = Set(
        60482457,
        'Rando 1 3 - Rando 2 0',
        None,
        3,
        -6,
        9,
        12687800,
        [e3, e4],
        None,
    )

    ut = get_upset_thread([winners_set, losers_set, notables_set, dqs_set, others_set])

    assert set_to_upset_thread_item(winners_set) in ut.winners
    assert set_to_upset_thread_item(losers_set) in ut.losers
    assert set_to_upset_thread_item(notables_set) in ut.notables
    assert set_to_upset_thread_item(dqs_set) in ut.dqs
    assert set_to_upset_thread_item(others_set) in ut.other


def test_submit_to_subreddit_1():
    pass


def test_add_sets_1():
    pass


def test_get_upset_thread_redis_1(mock_events_redis_db):
    pass
    # mock_events_redis_db.return_value = []
    # upset_thread = get_upset_thread_redis("tournament/battle-of-bc-5-5/event/ultimate-singles")
    # print(upset_thread)
