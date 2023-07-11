import json

import settings
from src.integrations.startgg.api import get_event
from mapper import to_domain_set, to_markdown
from time import sleep
from requests.exceptions import HTTPError
from src.service import get_upset_thread, init_app_state, submit_to_subreddit

slug = 'tournament/battle-of-bc-5-5/event/ultimate-singles'
title = 'Battle of BC 5 Ultimate Singles Upset Thread'
# slug = 'tournament/high-rez/event/smash-ultimate-singles-day-two'
# title = 'High Rez Ultimate Singles Day 2 Upset Thread'
subreddit = f'u_{settings.REDDIT_USERNAME}'
sets = []
page = 1
use_cache = False


init_app_state(slug)


if use_cache:
    with open('src/data/startgg_data.json', 'r') as data:
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

upset_thread = get_upset_thread(sets)

md = to_markdown(upset_thread)


with open('test.md', 'w') as file:
    file.write(md)


submit_to_subreddit(subreddit, title, md)


# subreddit = reddit.subreddit(f'u_{settings.REDDIT_USERNAME}')

# subreddit.submit(title="Test", selftext=md)

# submission = reddit.submission("14wynpr")

# submission.edit(md)
