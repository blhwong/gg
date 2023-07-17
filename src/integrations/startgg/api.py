from src.integrations.startgg.query import events_query, characters_query


class StartGGClient:

    def __init__(self, request_client, api_url, start_gg_api_key):
        self.request_client = request_client
        self.api_url = api_url
        self.start_gg_api_key = start_gg_api_key

    def get_event(self, slug, page=None):
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

    def get_characters(self):
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
