import pytest
from unittest.mock import ANY
from src.integrations.startgg.api import get_event, get_characters, api_url
from src.integrations.startgg.query import events_query, characters_query


@pytest.fixture
def mock_requests(mocker):
    return mocker.patch('src.integrations.startgg.api.requests')


def test_get_event_1(mock_requests):
    get_event('slug', 5)
    expected_payload = {
        'query': events_query,
        'variables': {
            'slug': 'slug',
            'page': 5,
            'filters': {
                'state': 3,
            },
            'sortType': 'RECENT'
        }
    }
    mock_requests.post.assert_called_with(api_url, json=expected_payload, headers=ANY)


def test_get_characters_1(mock_requests):
    get_characters()
    expected_payload = {
        'query': characters_query,
        'variables': {
            'slug': 'game/ultimate',
        },
    }
    mock_requests.post.assert_called_with(api_url, json=expected_payload, headers=ANY)
