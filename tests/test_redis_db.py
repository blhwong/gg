import pytest
from src.data.redis_db import CharactersRedisDb, EventsRedisDb, EventSetsRedisDb


@pytest.fixture
def mock_redis(mocker):
    return mocker.patch('src.data.redis_db.r')


def test_is_characters_loaded_1(mock_redis):
    mock_redis.get.return_value = '1'
    characters_redis_db = CharactersRedisDb()
    assert characters_redis_db.is_characters_loaded()


def test_is_characters_loaded_2(mock_redis):
    mock_redis.get.return_value = None
    characters_redis_db = CharactersRedisDb()
    assert not characters_redis_db.is_characters_loaded()


def test_set_is_character_loaded_1(mock_redis):
    characters_redis_db = CharactersRedisDb()
    characters_redis_db.set_is_characters_loaded(1)
    mock_redis.set.assert_called_with("is_character_loaded", 1)


def test_add_characters_1(mock_redis):
    characters = [{'id': 1234, 'name': 'Cloud'}]
    characters_redis_db = CharactersRedisDb()
    characters_redis_db.add_characters(characters)
    mock_redis.set.assert_called_with('character:1234', 'Cloud')


def test_get_character_name_1(mock_redis):
    characters_redis_db = CharactersRedisDb()
    characters_redis_db.get_character_name(1234)
    mock_redis.get.assert_called_with('character:1234')


def test_get_last_updated_date_1(mock_redis):
    events_redis_db = EventsRedisDb()
    events_redis_db.get_last_updated_date('slug')
    mock_redis.hget.assert_called_with('event:slug', 'last_updated_date')


def test_set_last_updated_date_1(mock_redis):
    events_redis_db = EventsRedisDb()
    events_redis_db.set_last_updated_date('slug', 1234)
    mock_redis.hset.assert_called_with('event:slug', 'last_updated_date', 1234)


def test_set_created_at_1(mock_redis):
    events_redis_db = EventsRedisDb()
    events_redis_db.set_created_at('slug', 2345)
    mock_redis.hset.assert_called_with('event:slug', 'created_at', 2345)


def test_get_submission_id_1(mock_redis):
    events_redis_db = EventsRedisDb()
    events_redis_db.get_submission_id('slug')
    mock_redis.hget.assert_called_with('event:slug', 'submission_id')


def test_set_submission_id_1(mock_redis):
    events_redis_db = EventsRedisDb()
    events_redis_db.set_submission_id('slug', 'abcd')
    mock_redis.hset.assert_called_with('event:slug', 'submission_id', 'abcd')


def test_add_sets_1(mock_redis):
    event_sets_redis_db = EventSetsRedisDb()
    mapping = {
        '1234': 'a,b,c,d'
    }
    event_sets_redis_db.add_sets('slug', mapping)
    mock_redis.hset.assert_called_with('event:slug_sets', '1234', 'a,b,c,d')


def test_get_sets_1(mock_redis):
    event_sets_redis_db = EventSetsRedisDb()
    event_sets_redis_db.get_sets('slug')
    mock_redis.hgetall.assert_called_with('event:slug_sets')
