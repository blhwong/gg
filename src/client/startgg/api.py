import requests

from src.client.startgg.query import events_query, characters_query


class StartGGClient:

    def __init__(self, request_client: requests, api_url: str, start_gg_api_key: str) -> None:
        self.request_client = request_client
        self.api_url = api_url
        self.start_gg_api_key = start_gg_api_key

    def get_event(self, slug: str, page: int = None) -> object:
        payload = {
            'query': events_query,
            'variables': {
                'slug': slug,
                'page': page,
                'filters': {
                    'state': 3
                },
                'sortType': 'RECENT'
            }
        }
        headers = {
            'Authorization': f'Bearer {self.start_gg_api_key}',
            'Content-Type': 'application/json',
        }
        res = self.request_client.post(self.api_url, json=payload, headers=headers)
        if res.status_code != 200:
            res.raise_for_status()
        return res.json()

    def get_characters(self) -> object:
        payload = {
            'query': characters_query,
            'variables': {
                'slug': 'game/ultimate',
            },
        }
        headers = {
            'Authorization': f'Bearer {self.start_gg_api_key}',
            'Content-Type': 'application/json',
        }
        res = self.request_client.post(self.api_url, json=payload, headers=headers)
        if res.status_code != 200:
            res.raise_for_status()
        return res.json()
