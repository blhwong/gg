import json
from src.startgg.api import get_event
from mapper import to_domain_set, to_markdown, to_markdown_table
from db import SetsInMemoryDb
from time import sleep
from requests.exceptions import HTTPError

# slug = 'tournament/high-rez/event/smash-ultimate-singles-day-two'
slug = 'tournament/battle-of-bc-5-5/event/ultimate-singles'
sets = []
page = 1
use_cache = True

sets_db = SetsInMemoryDb()

if use_cache:
    with open('data/startgg_data.json', 'r') as data:
        sets += [to_domain_set(s) for s in json.load(data)]
    data.close()
else:
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

md_table = to_markdown_table(upset_thread)

# print(md)

with open('test.md', 'w') as file:
    file.write(md)

with open('test_table.md', 'w') as table:
    table.write(md_table)
