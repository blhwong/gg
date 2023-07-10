from api import get_event
from mapper import to_domain_set, to_markdown
from db import SetsInMemoryDb

slug = 'tournament/high-rez/event/smash-ultimate-singles-day-two'
sets = []
page = 1
fetch = True

sets_db = SetsInMemoryDb()

while fetch:
    res = get_event(slug, page)
    if 'errors' in res:
        print(res['errors'])
        break
    total_pages = res['data']['event']['sets']['pageInfo']['totalPages']
    if page > total_pages:
        break
    page += 1
    sets += [to_domain_set(s) for s in res['data']['event']['sets']['nodes']]


sets.sort(key=lambda s: -s.upset_factor)

sets_db.add_sets(sets)

upset_thread = sets_db.get_upset_thread({
    'min_upset_factor': 1,
})

md = to_markdown(upset_thread)

print(md)
