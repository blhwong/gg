# from src.data.redis_db import EventsRedisDb
from src.domain import Set, Entrant, Selection, Character
from src.service import get_upset_thread, submit_to_subreddit, add_sets, get_upset_thread_redis, get_character_name
from src.mapper.upset_thread_mapper import set_to_upset_thread_item
from src.data.redis_mapper import upset_thread_item_to_redis_set

e1 = Entrant(12394650, 'LG | Tweek', 3)
e2 = Entrant(12687800, 'Zomba', 20)
s1 = [Selection(e1, Character(1279, 'Diddy Kong')), Selection(e2, Character(1323, 'R.O.B.'))]
s2 = [Selection(e1, Character(1777, 'Sephiroth')), Selection(e2, Character(1323, 'R.O.B.'))]

e3 = Entrant(12394650, 'Rando 1', 100)
e4 = Entrant(12687800, 'Rando 2', 200)
s3 = [Selection(e1, Character(1279, 'Diddy Kong')), Selection(e2, Character(1323, 'R.O.B.'))]
s4 = [Selection(e1, Character(1777, 'Sephiroth')), Selection(e2, Character(1323, 'R.O.B.'))]

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


def test_get_upset_thread_1():
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


def test_get_upset_thread_redis_1(mocker):
    winner = set_to_upset_thread_item(winners_set)
    loser = set_to_upset_thread_item(losers_set)
    notable = set_to_upset_thread_item(notables_set)
    dq = set_to_upset_thread_item(dqs_set)
    other = set_to_upset_thread_item(others_set)
    redis_sets = {
        f'winners:{winners_set.id}': upset_thread_item_to_redis_set(winner),
        f'losers:{losers_set.id}': upset_thread_item_to_redis_set(loser),
        f'notables:{notables_set.id}': upset_thread_item_to_redis_set(notable),
        f'dqs:{dqs_set.id}': upset_thread_item_to_redis_set(dq),
        f'other:{others_set.id}': upset_thread_item_to_redis_set(other),
    }
    mocker.patch('src.service.event_sets_redis_db.get_sets', return_value=redis_sets)
    upset_thread = get_upset_thread_redis("tournament/battle-of-bc-5-5/event/ultimate-singles")
    assert winner in upset_thread.winners
    assert loser in upset_thread.losers
    assert notable in upset_thread.notables
    assert dq in upset_thread.dqs
    assert other in upset_thread.other


def test_get_character_name_1():
    pass
