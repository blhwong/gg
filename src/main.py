import json

from src.integrations.startgg.api import get_event
from mapper import to_domain_set, to_markdown
from time import sleep
from requests.exceptions import HTTPError
from src.service import get_upset_thread

# slug = 'tournament/high-rez/event/smash-ultimate-singles-day-two'
slug = 'tournament/battle-of-bc-5-5/event/ultimate-singles'
sets = []
page = 1
use_cache = True


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



# subreddit = reddit.subreddit(f'u_{settings.REDDIT_USERNAME}')

# subreddit.submit(title="Test", selftext=md)

# submission = reddit.submission("14wynpr")

# submission.edit(md)
