import json
from api import get_event
from service import calculate_upset_factors

page = 1
slug = 'tournament/high-rez/event/smash-ultimate-singles-day-two'

sets = []

res = get_event(slug, page)
sets += res['data']['event']['sets']['nodes']

while page < res['data']['event']['sets']['pageInfo']['totalPages']:
    page += 1
    print(page)
    res = get_event(slug, page)
    sets += res['data']['event']['sets']['nodes']


upset_factors = calculate_upset_factors(sets)

upset_factors.sort(key=lambda x: x['upset_factor'])

print(json.dumps(upset_factors, indent=4))
