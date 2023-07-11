from src.startgg.api import get_event
from mapper import to_domain_set, to_markdown
from db import SetsInMemoryDb
from time import sleep
from requests.exceptions import HTTPError

# slug = 'tournament/high-rez/event/smash-ultimate-singles-day-two'
slug = 'tournament/battle-of-bc-5-5/event/ultimate-singles'
sets = []
page = 1

sets_db = SetsInMemoryDb()

while True:
    print(page)
    sleep(0.75)
    try:
        res = get_event(slug, page)
    except HTTPError as e:
        print(e)
        continue
    if 'errors' in res:
        print(res['errors'])
        break
    total_pages = res['data']['event']['sets']['pageInfo']['totalPages']
    # total_pages = 2
    if page > total_pages:
        break
    page += 1
    sets += [to_domain_set(s) for s in res['data']['event']['sets']['nodes']]


sets.sort(key=lambda s: -s.upset_factor)

sets_db.add_sets(sets)

upset_thread = sets_db.get_upset_thread()

md = to_markdown(upset_thread)

# print(md)

with open('test.md', 'w') as file:
    file.write(md)
