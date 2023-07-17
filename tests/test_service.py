import pytest
from unittest.mock import Mock
from src.domain import Set, Entrant, Selection, Character, UpsetThread
from src.service import get_upset_thread, submit_to_subreddit, add_sets, get_upset_thread_redis, get_character_name
from src.mapper.upset_thread_mapper import set_to_upset_thread_item
from src.data.redis_mapper import upset_thread_item_to_redis_set

e1 = Entrant(12394650, 'LG | Tweek', 3, 9, True)
e2 = Entrant(12687800, 'Zomba', 20, 8, False)
s1 = [Selection(e1, Character(1279, 'Diddy Kong')), Selection(e2, Character(1323, 'R.O.B.'))]
s2 = [Selection(e1, Character(1777, 'Sephiroth')), Selection(e2, Character(1323, 'R.O.B.'))]

e3 = Entrant(12394650, 'Rando 1', 100, 49, False)
e4 = Entrant(12687800, 'Rando 2', 200, 65, True)
s3 = [Selection(e1, Character(1279, 'Diddy Kong')), Selection(e2, Character(1323, 'R.O.B.'))]
s4 = [Selection(e1, Character(1777, 'Sephiroth')), Selection(e2, Character(1323, 'R.O.B.'))]

winners_set = Set(
    60482457,
    'Zomba 3 - LG | Tweek 0',
    None,
    5,
    6,
    9,
    12687800,
    [e1, e2],
    None,
    None,
)
losers_set = Set(
    60482458,
    'Zomba 3 - LG | Tweek 0',
    None,
    5,
    -6,
    9,
    12687800,
    [e1, e2],
    None,
    None,
)
notables_set = Set(
    60482459,
    'LG | Tweek 3 - Zomba 2',
    None,
    5,
    6,
    9,
    12394650,
    [e1, e2],
    None,
    None,
)
dqs_set = Set(
    60482460,
    'DQ',
    None,
    5,
    -6,
    9,
    12687800,
    [e1, e2],
    None,
    None,
)
others_set = Set(
    60482461,
    'Rando 1 3 - Rando 2 0',
    None,
    5,
    -6,
    9,
    12687800,
    [e3, e4],
    None,
    None,
)


@pytest.fixture
def mock_events_redis_db(mocker):
    return mocker.patch('src.service.events_redis_db')


@pytest.fixture
def mock_reddit(mocker):
    return mocker.patch('src.service.reddit')


@pytest.fixture
def mock_event_sets_redis_db(mocker):
    return mocker.patch('src.service.event_sets_redis_db')


def test_get_upset_thread_1():
    ut = get_upset_thread([winners_set, losers_set, notables_set, dqs_set, others_set])

    assert set_to_upset_thread_item(winners_set, 'winners') in ut.winners
    assert set_to_upset_thread_item(losers_set, 'losers') in ut.losers
    assert set_to_upset_thread_item(notables_set, 'notables') in ut.notables
    assert set_to_upset_thread_item(dqs_set, 'dqs') in ut.dqs
    assert set_to_upset_thread_item(others_set, 'other') in ut.other


def test_submit_to_subreddit_1(mock_events_redis_db, mock_reddit):
    mock_events_redis_db.get_submission_id.return_value = '1234'
    mock_reddit.submission.return_value = Mock()
    submit_to_subreddit('slug', 'test', 'My title', 'my md')

    mock_reddit.submission.return_value.edit.assert_called_with('my md')
    mock_events_redis_db.set_last_updated_date.assert_called_once()


def test_submit_to_subreddit_2(mock_events_redis_db, mock_reddit):
    mock_events_redis_db.get_submission_id.return_value = None
    mock_reddit.subreddit.return_value = Mock()
    submit_to_subreddit('slug', 'test', 'My title', 'my md')

    mock_events_redis_db.set_last_updated_date.assert_called_once()
    mock_reddit.subreddit.return_value.submit.assert_called_with(title='My title', selftext='my md')
    mock_events_redis_db.set_submission_id.assert_called_once()
    mock_events_redis_db.set_created_at.assert_called_once()


def test_submit_to_subreddit_3(mock_events_redis_db):
    mock_events_redis_db.get_submission_id.return_value = None
    mock_events_redis_db.set_last_updated_date.return_value = None
    with pytest.raises(Exception) as exception_info:
        submit_to_subreddit('slug', 'test', None, 'my md')

    assert str(exception_info.value) == 'Title is required.'


def test_add_sets_1(mock_event_sets_redis_db):
    winner = set_to_upset_thread_item(winners_set, 'winners')
    loser = set_to_upset_thread_item(losers_set, 'losers')
    notable = set_to_upset_thread_item(notables_set, 'notables')
    dq = set_to_upset_thread_item(dqs_set, 'dqs')
    other = set_to_upset_thread_item(others_set, 'other')
    expected_redis_sets = {
        winners_set.id: upset_thread_item_to_redis_set(winner, 'winners'),
        losers_set.id: upset_thread_item_to_redis_set(loser, 'losers'),
        notables_set.id: upset_thread_item_to_redis_set(notable, 'notables'),
        dqs_set.id: upset_thread_item_to_redis_set(dq, 'dqs'),
        others_set.id: upset_thread_item_to_redis_set(other, 'other'),
    }
    upset_thread = UpsetThread(
        [winner],
        [loser],
        [notable],
        [dq],
        [other],
    )
    add_sets('test_slug', upset_thread)
    mock_event_sets_redis_db.add_sets.assert_called_with('test_slug', expected_redis_sets)


def test_get_upset_thread_redis_1(mock_event_sets_redis_db):
    winner = set_to_upset_thread_item(winners_set, 'winners')
    loser = set_to_upset_thread_item(losers_set, 'losers')
    notable = set_to_upset_thread_item(notables_set, 'notables')
    dq = set_to_upset_thread_item(dqs_set, 'dqs')
    other = set_to_upset_thread_item(others_set, 'other')
    redis_sets = {
        winners_set.id: upset_thread_item_to_redis_set(winner, 'winners'),
        losers_set.id: upset_thread_item_to_redis_set(loser, 'losers'),
        notables_set.id: upset_thread_item_to_redis_set(notable, 'notables'),
        dqs_set.id: upset_thread_item_to_redis_set(dq, 'dqs'),
        others_set.id: upset_thread_item_to_redis_set(other, 'other'),
    }
    mock_event_sets_redis_db.get_sets.return_value = redis_sets
    upset_thread = get_upset_thread_redis("tournament/battle-of-bc-5-5/event/ultimate-singles")
    assert winner in upset_thread.winners
    assert loser in upset_thread.losers
    assert notable in upset_thread.notables
    assert dq in upset_thread.dqs
    assert other in upset_thread.other


def test_get_character_name_1(mocker):
    mocker.patch('src.service.get_characters', return_value={'data': {'videogame': {'characters': []}}})
    mock_characters_redis_db = mocker.patch('src.service.characters_redis_db')
    mock_characters_redis_db.is_characters_loaded.return_value = False
    mock_characters_redis_db.get_character_name.return_value = 'Cloud'

    name = get_character_name(1234)

    assert name == 'Cloud'

    mock_characters_redis_db.set_is_characters_loaded.assert_called_once()
    mock_characters_redis_db.add_characters.assert_called_with([])
    mock_characters_redis_db.get_character_name.assert_called_with(1234)
