import json
from api import get_event
from service import calculate_upset_factors

slug = 'tournament/high-rez/event/smash-ultimate-singles-day-two'

sets = []

page = 1

while True:
    print(page)
    res = get_event(slug, page)
    if 'errors' in res:
        print(res['errors'])
        break
    if page > res['data']['event']['sets']['pageInfo']['totalPages']:
        print('Done')
        break
    page += 1
    sets += res['data']['event']['sets']['nodes']


upset_factors = calculate_upset_factors(sets)

upset_factors.sort(key=lambda x: x['upset_factor'])

print(json.dumps(upset_factors, indent=4))
