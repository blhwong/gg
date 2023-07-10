import json
from api import get_event
from mapper import to_domain_set

slug = 'tournament/high-rez/event/smash-ultimate-singles-day-two'

sets = []

page = 1

while True:
    print(page)
    res = get_event(slug, page)
    if 'errors' in res:
        print(res['errors'])
        break
    total_pages = res['data']['event']['sets']['pageInfo']['totalPages']
    if page > total_pages:
        print('Done')
        break
    page += 1
    sets += [to_domain_set(s) for s in res['data']['event']['sets']['nodes']]


sets.sort(key=lambda s: s.upset_factor)

print(sets)
print(len(sets))
