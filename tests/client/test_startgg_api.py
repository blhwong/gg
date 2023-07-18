from unittest.mock import ANY, Mock

import pytest

from src.client.startgg.api import StartGGClient
from src.client.startgg.query import events_query, characters_query

test_api_url = 'https://test.com'


@pytest.fixture
def mock_startgg_client():
    return StartGGClient(Mock(), test_api_url, 'test_api_key')


def test_get_event_1(mock_startgg_client):
    mock_startgg_client.get_event('slug', 5)
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
    mock_startgg_client.request_client.post.assert_called_with(test_api_url, json=expected_payload, headers=ANY)


def test_get_characters_1(mock_startgg_client):
    mock_startgg_client.get_characters()
    expected_payload = {
        'query': characters_query,
        'variables': {
            'slug': 'game/ultimate',
        },
    }
    mock_startgg_client.request_client.post.assert_called_with(test_api_url, json=expected_payload, headers=ANY)
