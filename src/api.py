import requests
import os
from dotenv import load_dotenv


load_dotenv()


query = """
    query EventQuery(
        $slug: String 
        $filters: SetFilters
        $page: Int
        $sortType: SetSortType
    ) {
        event(slug: $slug) {
            id
            slug
            sets(filters: $filters page: $page sortType: $sortType) {
                pageInfo {
                    total
                    totalPages
                    page
                    perPage
                    sortBy
                    filter
                }
                nodes {
                    id
                    completedAt
                    games {
                        winnerId
                    }
                    identifier
                    displayScore
                    fullRoundText
                    totalGames
                    lPlacement
                    wPlacement
                    winnerId
                    state
                    setGamesType
                    round
                    phaseGroup {
                        displayIdentifier
                    }
                    slots {
                        entrant {
                            id
                            name
                            initialSeedNum
                        }
                    }
                }
            }
        }
    }
"""


start_gg_api_key = os.environ.get("START_GG_API_KEY")
api_url = "https://api.start.gg/gql/alpha"


def get_event(slug, page=None):
    payload = {
        'query': query,
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
