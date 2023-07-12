import json
import argparse
import settings
from src.integrations.startgg.api import get_event
from src.mapper.markdown_mapper import to_markdown
from src.mapper.set_mapper import to_domain_set
from time import sleep
from requests.exceptions import HTTPError
from src.service import get_upset_thread, submit_to_subreddit, add_sets, get_upset_thread_redis

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--slug')
parser.add_argument('-t', '--title')
parser.add_argument('-sr', '--subreddit')
parser.add_argument('-f', '--file')

args = parser.parse_args()

# slug = 'tournament/battle-of-bc-5-5/event/ultimate-singles'
# title = 'Battle of BC 5 Ultimate Singles Upset Thread'
# slug = 'tournament/high-rez/event/smash-ultimate-singles-day-two'
# title = 'High Rez Ultimate Singles Day 2 Upset Thread'
# subreddit = f'u_{settings.REDDIT_USERNAME}'


def process(slug, title, subreddit, file):
    sets = []
    page = 1
    if file:
        print('Using file data')
        with open('src/data/startgg_data.json', 'r') as data:
            sets += [to_domain_set(s) for s in json.load(data)]
        data.close()
    else:
        print('Fetching data from startgg')
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
            if page > total_pages:
                break
            page += 1
            sets += [to_domain_set(s) for s in res['data']['event']['sets']['nodes']]

    sets.sort(key=lambda s: -s.upset_factor)
    upset_thread = get_upset_thread(sets)
    add_sets(slug, upset_thread)
    saved_upset_thread = get_upset_thread_redis(slug)
    md = to_markdown(saved_upset_thread, slug)

    with open(f'output'
              f'/{title}.md', 'w+') as file:
        file.write(md)

    if subreddit:
        print(f'Posting to subreddit {subreddit}')
        submit_to_subreddit(slug, subreddit, title, md)
    else:
        print('Skipping post to subreddit')


process(args.slug, args.title, args.subreddit, args.file)
