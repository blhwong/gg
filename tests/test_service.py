import pytest
from unittest.mock import Mock
from src.domain import Set, Entrant, Selection, Character, UpsetThread
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


def test_submit_to_subreddit_1(mocker):
    mocker.patch('src.service.events_redis_db.get_submission_id', return_value='1234')
    mock_set_last_updated_date = mocker.patch('src.service.events_redis_db.set_last_updated_date')
    mock = mocker.patch('src.service.reddit.submission', return_value=Mock())
    submit_to_subreddit('slug', 'test', 'My title', 'my md')

    mock.return_value.edit.assert_called_with('my md')
    mock_set_last_updated_date.assert_called_once()


def test_submit_to_subreddit_2(mocker):
    mocker.patch('src.service.events_redis_db.get_submission_id', return_value=None)
    mock_set_last_updated_date = mocker.patch('src.service.events_redis_db.set_last_updated_date')
    mock = mocker.patch('src.service.reddit.subreddit', return_value=Mock())
    mock_set_submission_id = mocker.patch('src.service.events_redis_db.set_submission_id')
    mock_set_created_at = mocker.patch('src.service.events_redis_db.set_created_at')
    submit_to_subreddit('slug', 'test', 'My title', 'my md')

    mock_set_last_updated_date.assert_called_once()
    mock.return_value.submit.assert_called_with(title='My title', selftext='my md')
    mock_set_submission_id.assert_called_once()
    mock_set_created_at.assert_called_once()


def test_submit_to_subreddit_3(mocker):
    mocker.patch('src.service.events_redis_db.get_submission_id', return_value=None)
    mocker.patch('src.service.events_redis_db.set_last_updated_date')
    with pytest.raises(Exception) as exception_info:
        submit_to_subreddit('slug', 'test', None, 'my md')

    assert str(exception_info.value) == 'Title is required.'


def test_add_sets_1(mocker):
    winner = set_to_upset_thread_item(winners_set)
    loser = set_to_upset_thread_item(losers_set)
    notable = set_to_upset_thread_item(notables_set)
    dq = set_to_upset_thread_item(dqs_set)
    other = set_to_upset_thread_item(others_set)
    expected_redis_sets = {
        f'winners:{winners_set.id}': upset_thread_item_to_redis_set(winner),
        f'losers:{losers_set.id}': upset_thread_item_to_redis_set(loser),
        f'notables:{notables_set.id}': upset_thread_item_to_redis_set(notable),
        f'dqs:{dqs_set.id}': upset_thread_item_to_redis_set(dq),
        f'other:{others_set.id}': upset_thread_item_to_redis_set(other),
    }
    upset_thread = UpsetThread(
        [winner],
        [loser],
        [notable],
        [dq],
        [other],
    )
    mock = mocker.patch('src.service.event_sets_redis_db.add_sets')
    add_sets('test_slug', upset_thread)
    mock.assert_called_with('test_slug', expected_redis_sets)


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


def test_get_character_name_1(mocker):
    mocker.patch('src.service.characters_redis_db.is_characters_loaded', return_value=False)
    mocker.patch('src.service.get_characters', return_value={'data':{'videogame':{'characters': []}}})
    mock_add_characters = mocker.patch('src.service.characters_redis_db.add_characters')
    mock_set_is_characters_loaded = mocker.patch('src.service.characters_redis_db.set_is_characters_loaded')
    mock_get_character_name = mocker.patch('src.service.characters_redis_db.get_character_name', return_value='Cloud')

    name = get_character_name(1234)

    assert name == 'Cloud'
    mock_set_is_characters_loaded.assert_called_once()
    mock_add_characters.assert_called_with([])
    mock_get_character_name.assert_called_with(1234)