from unittest.mock import Mock

import pytest

from src.data.redis_db import RedisService


@pytest.fixture
def mock_redis_service():
    return RedisService(Mock())


def test_is_characters_loaded_1(mock_redis_service):
    mock_redis_service.r.get.return_value = '1'
    assert mock_redis_service.is_characters_loaded()


def test_is_characters_loaded_2(mock_redis_service):
    mock_redis_service.r.get.return_value = None
    assert not mock_redis_service.is_characters_loaded()


def test_set_is_character_loaded_1(mock_redis_service):
    mock_redis_service.set_is_characters_loaded(1)
    mock_redis_service.r.set.assert_called_with("is_character_loaded", 1)


def test_add_characters_1(mock_redis_service):
    characters = [{'id': 1234, 'name': 'Cloud'}]
    mock_redis_service.add_characters(characters)
    mock_redis_service.r.set.assert_called_with('character:1234', 'Cloud')


def test_get_character_name_1(mock_redis_service):
    mock_redis_service.get_character_name(1234)
    mock_redis_service.r.get.assert_called_with('character:1234')


def test_get_last_updated_date_1(mock_redis_service):
    mock_redis_service.get_last_updated_date('slug')
    mock_redis_service.r.hget.assert_called_with('event:slug', 'last_updated_date')


def test_set_last_updated_date_1(mock_redis_service):
    mock_redis_service.set_last_updated_date('slug', 1234)
    mock_redis_service.r.hset.assert_called_with('event:slug', 'last_updated_date', 1234)


def test_set_created_at_1(mock_redis_service):
    mock_redis_service.set_created_at('slug', 2345)
    mock_redis_service.r.hset.assert_called_with('event:slug', 'created_at', 2345)


def test_get_submission_id_1(mock_redis_service):
    mock_redis_service.get_submission_id('slug')
    mock_redis_service.r.hget.assert_called_with('event:slug', 'submission_id')


def test_set_submission_id_1(mock_redis_service):
    mock_redis_service.set_submission_id('slug', 'abcd')
    mock_redis_service.r.hset.assert_called_with('event:slug', 'submission_id', 'abcd')


def test_add_sets_1(mock_redis_service):
    mapping = {
        '1234': 'a,b,c,d'
    }
    mock_redis_service.add_sets('slug', mapping)
    mock_redis_service.r.hset.assert_called_with('event:slug_sets', '1234', 'a,b,c,d')


def test_get_sets_1(mock_redis_service):
    mock_redis_service.get_sets('slug')
    mock_redis_service.r.hgetall.assert_called_with('event:slug_sets')
