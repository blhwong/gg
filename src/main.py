import argparse
import json
from time import sleep, time

import redis
import requests
from requests.exceptions import HTTPError

import settings
from logger import logging
from src.client.reddit.api import reddit
from src.client.startgg.api import StartGGClient
from src.data.redis_db import RedisService
from src.mapper.markdown_mapper import to_markdown
from src.service import Service

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--slug')
parser.add_argument('-t', '--title')
parser.add_argument('-sr', '--subreddit')
parser.add_argument('-f', '--file')
parser.add_argument('-fm', '--frequency_minutes', type=int)

args = parser.parse_args()

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
redis_service = RedisService(r)
startgg_client = StartGGClient(requests, settings.START_GG_API_URL, settings.START_GG_API_KEY)
service = Service(redis_service, reddit, startgg_client)


def process(slug: str, title: str, subreddit: str, file: str):
    sets = []
    page = 1
    if file:
        logger.info('Using file data')
        with open('src/data/startgg_data.json', 'r') as data:
            sets += [service.to_domain_set(s) for s in json.load(data)]
        data.close()
    else:
        logger.info('Fetching data from startgg')
        while True:
            logger.debug(f'Fetching page {page}')
            sleep(0.80)
            try:
                res = service.get_event(slug, page)
            except HTTPError as e:
                logger.warning(e)
                continue
            if 'errors' in res:
                logger.error(res['errors'])
                break
            total_pages = res['data']['event']['sets']['pageInfo']['totalPages']
            if page > total_pages:
                break
            page += 1
            sets += [service.to_domain_set(s) for s in res['data']['event']['sets']['nodes']]

    sets.sort(key=lambda s: -s.upset_factor)
    upset_thread = service.get_upset_thread(sets)
    service.add_sets(slug, upset_thread)
    saved_upset_thread = service.get_upset_thread_db(slug)
    md = to_markdown(saved_upset_thread, slug)

    with open(f'output/{int(time())} {title}.md', 'w+') as file:
        logger.info('Saving md to output')
        file.write(md)

    if subreddit:
        logger.info(f'Posting to subreddit {subreddit}')
        service.submit_to_subreddit(slug, subreddit, title, md)
    else:
        logger.info('Skipping post to subreddit')


while True:
    logger.info('Starting...')
    process(args.slug, args.title, args.subreddit, args.file)
    logger.info('Done!')
    sleep(args.frequency_minutes * 60)
