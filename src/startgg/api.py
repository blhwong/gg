import requests
import os
from dotenv import load_dotenv
from src.startgg.query import events_query, characters_query


load_dotenv()

start_gg_api_key = os.environ.get("START_GG_API_KEY")
api_url = "https://api.start.gg/gql/alpha"


def get_event(slug, page=None):
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
        'Authorization': f'Bearer {start_gg_api_key}',
        'Content-Type': 'application/json',
    }
    res = requests.post(api_url, json=payload, headers=headers)
    if res.status_code != 200:
        res.raise_for_status()
    return res.json()


def get_characters():
    payload = {
        'query': characters_query,
        'variables': {
            'slug': 'game/ultimate',
        },
    }
    headers = {
        'Authorization': f'Bearer {start_gg_api_key}',
        'Content-Type': 'application/json',
    }
    res = requests.post(api_url, json=payload, headers=headers)
    if res.status_code != 200:
        res.raise_for_status()
    return res.json()
