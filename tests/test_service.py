from unittest.mock import Mock

import pytest

from src.data.redis_mapper import upset_thread_item_to_redis_set
from src.domain.set import Set, Entrant, Selection, Character, Game
from src.domain.upset_thread import UpsetThread
from src.mapper.upset_thread_mapper import set_to_upset_thread_item
from src.service import Service

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
def mock_service():
    return Service(Mock(), Mock(), Mock())


def test_get_upset_thread_1(mock_service):
    ut = mock_service.get_upset_thread([winners_set, losers_set, notables_set, dqs_set, others_set])

    assert set_to_upset_thread_item(winners_set, 'winners') in ut.winners
    assert set_to_upset_thread_item(losers_set, 'losers') in ut.losers
    assert set_to_upset_thread_item(notables_set, 'notables') in ut.notables
    assert set_to_upset_thread_item(dqs_set, 'dqs') in ut.dqs
    assert set_to_upset_thread_item(others_set, 'other') in ut.other


def test_submit_to_subreddit_1(mock_service):
    mock_service.db_service.get_submission_id.return_value = '1234'
    mock_service.reddit_client.submission.return_value = Mock()
    mock_service.submit_to_subreddit('slug', 'test', 'My title', 'my md')

    mock_service.reddit_client.submission.return_value.edit.assert_called_with('my md')
    mock_service.db_service.set_last_updated_date.assert_called_once()


def test_submit_to_subreddit_2(mock_service):
    mock_service.db_service.get_submission_id.return_value = None
    mock_service.reddit_client.subreddit.return_value = Mock()
    mock_service.submit_to_subreddit('slug', 'test', 'My title', 'my md')

    mock_service.db_service.set_last_updated_date.assert_called_once()
    mock_service.reddit_client.subreddit.return_value.submit.assert_called_with(title='My title', selftext='my md')
    mock_service.db_service.set_submission_id.assert_called_once()
    mock_service.db_service.set_created_at.assert_called_once()


def test_submit_to_subreddit_3(mock_service):
    mock_service.db_service.get_submission_id.return_value = None
    mock_service.db_service.set_last_updated_date.return_value = None
    with pytest.raises(Exception) as exception_info:
        mock_service.submit_to_subreddit('slug', 'test', None, 'my md')

    assert str(exception_info.value) == 'Title is required.'


def test_add_sets_1(mock_service):
    winner = set_to_upset_thread_item(winners_set, 'winners')
    loser = set_to_upset_thread_item(losers_set, 'losers')
    notable = set_to_upset_thread_item(notables_set, 'notables')
    dq = set_to_upset_thread_item(dqs_set, 'dqs')
    other = set_to_upset_thread_item(others_set, 'other')
    expected_redis_sets = {
        winners_set.id: upset_thread_item_to_redis_set(winner),
        losers_set.id: upset_thread_item_to_redis_set(loser),
        notables_set.id: upset_thread_item_to_redis_set(notable),
        dqs_set.id: upset_thread_item_to_redis_set(dq),
        others_set.id: upset_thread_item_to_redis_set(other),
    }
    upset_thread = UpsetThread(
        [winner],
        [loser],
        [notable],
        [dq],
        [other],
    )
    mock_service.add_sets('test_slug', upset_thread)
    mock_service.db_service.add_sets.assert_called_with('test_slug', expected_redis_sets)


def test_get_upset_thread_redis_1(mock_service):
    winner = set_to_upset_thread_item(winners_set, 'winners')
    loser = set_to_upset_thread_item(losers_set, 'losers')
    notable = set_to_upset_thread_item(notables_set, 'notables')
    dq = set_to_upset_thread_item(dqs_set, 'dqs')
    other = set_to_upset_thread_item(others_set, 'other')
    redis_sets = {
        winners_set.id: upset_thread_item_to_redis_set(winner),
        losers_set.id: upset_thread_item_to_redis_set(loser),
        notables_set.id: upset_thread_item_to_redis_set(notable),
        dqs_set.id: upset_thread_item_to_redis_set(dq),
        others_set.id: upset_thread_item_to_redis_set(other),
    }
    mock_service.db_service.get_sets.return_value = redis_sets
    upset_thread = mock_service.get_upset_thread_db("tournament/battle-of-bc-5-5/event/ultimate-singles")
    assert winner in upset_thread.winners
    assert loser in upset_thread.losers
    assert notable in upset_thread.notables
    assert dq in upset_thread.dqs
    assert other in upset_thread.other


def test_get_character_name_1(mock_service):
    mock_service.startgg_client.get_characters.return_value = {'data': {'videogame': {'characters': []}}}
    mock_service.db_service.is_characters_loaded.return_value = False
    mock_service.db_service.get_character_name.return_value = 'Cloud'

    name = mock_service.get_character_name(1234)

    assert name == 'Cloud'

    mock_service.db_service.set_is_characters_loaded.assert_called_once()
    mock_service.db_service.add_characters.assert_called_with([])
    mock_service.db_service.get_character_name.assert_called_with(1234)


def test_to_domain_set(mock_service):
    characters = {
        1337: 'Wolf',
        1316: 'Palutena',
        1341: 'Zero Suit Samus',
    }
    mock_service.db_service.get_character_name.side_effect = lambda x: characters[x]
    s = mock_service.to_domain_set({
        "id": 62697291,
        "completedAt": 1689457041,
        "games": [
            {
                "id": 17627547,
                "winnerId": 13501615,
                "selections": [
                    {
                        "selectionType": "CHARACTER",
                        "selectionValue": 1337,
                        "entrant": {
                            "id": 13501615,
                            "name": "DOOB | idlehands",
                            "initialSeedNum": 93,
                            "standing": {
                                "isFinal": True,
                                "placement": 65
                            }
                        }
                    },
                    {
                        "selectionType": "CHARACTER",
                        "selectionValue": 1316,
                        "entrant": {
                            "id": 13634542,
                            "name": "Smoge | Be Kind",
                            "initialSeedNum": 164,
                            "standing": {
                                "isFinal": True,
                                "placement": 129
                            }
                        }
                    }
                ]
            },
            {
                "id": 17627548,
                "winnerId": 13501615,
                "selections": [
                    {
                        "selectionType": "CHARACTER",
                        "selectionValue": 1337,
                        "entrant": {
                            "id": 13501615,
                            "name": "DOOB | idlehands",
                            "initialSeedNum": 93,
                            "standing": {
                                "isFinal": True,
                                "placement": 65
                            }
                        }
                    },
                    {
                        "selectionType": "CHARACTER",
                        "selectionValue": 1341,
                        "entrant": {
                            "id": 13634542,
                            "name": "Smoge | Be Kind",
                            "initialSeedNum": 164,
                            "standing": {
                                "isFinal": True,
                                "placement": 129
                            }
                        }
                    }
                ]
            },
            {
                "id": 17627549,
                "winnerId": 13501615,
                "selections": [
                    {
                        "selectionType": "CHARACTER",
                        "selectionValue": 1337,
                        "entrant": {
                            "id": 13501615,
                            "name": "DOOB | idlehands",
                            "initialSeedNum": 93,
                            "standing": {
                                "isFinal": True,
                                "placement": 65
                            }
                        }
                    },
                    {
                        "selectionType": "CHARACTER",
                        "selectionValue": 1341,
                        "entrant": {
                            "id": 13634542,
                            "name": "Smoge | Be Kind",
                            "initialSeedNum": 164,
                            "standing": {
                                "isFinal": True,
                                "placement": 129
                            }
                        }
                    }
                ]
            }
        ],
        "identifier": "G",
        "displayScore": "DOOB | idlehands 3 - Smoge | Be Kind 0",
        "fullRoundText": "Winners Round 1",
        "totalGames": 5,
        "lPlacement": 13,
        "wPlacement": 9,
        "winnerId": 13501615,
        "state": 3,
        "setGamesType": 1,
        "round": 1,
        "phaseGroup": {
            "displayIdentifier": "B2"
        },
        "slots": [
            {
                "entrant": {
                    "id": 13501615,
                    "name": "DOOB | idlehands",
                    "initialSeedNum": 93,
                    "standing": {
                        "isFinal": True,
                        "placement": 65
                    }
                }
            },
            {
                "entrant": {
                    "id": 13634542,
                    "name": "Smoge | Be Kind",
                    "initialSeedNum": 164,
                    "standing": {
                        "isFinal": True,
                        "placement": 129
                    }
                }
            }
        ]
    })
    entrants = [
        Entrant(13501615, "DOOB | idlehands", 93, 65, True),
        Entrant(13634542, "Smoge | Be Kind", 164, 129, True)
    ]

    selection1 = Selection(entrants[0], Character(1337, 'Wolf'))
    selection2 = Selection(entrants[1], Character(1341, 'Zero Suit Samus'))
    selection3 = Selection(entrants[1], Character(1316, 'Palutena'))
    games = [
        Game(17627547, 13501615, [selection1, selection3]),
        Game(17627548, 13501615, [selection1, selection2]),
        Game(17627549, 13501615, [selection1, selection2]),
    ]
    assert s == Set(
        62697291,
        "DOOB | idlehands 3 - Smoge | Be Kind 0",
        "Winners Round 1",
        5,
        1,
        129,
        13501615,
        entrants,
        games,
        1689457041,
    )


def test_get_event_1(mock_service):
    mock_service.get_event('slug', 10)
    mock_service.startgg_client.get_event.assert_called_with('slug', 10)
