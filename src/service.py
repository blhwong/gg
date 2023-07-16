from time import time
from src.domain import UpsetThread
from src.data.redis_db import CharactersRedisDb, EventsRedisDb, EventSetsRedisDb
from src.integrations.startgg.api import get_characters
from src.integrations.reddit.api import reddit
from src.data.redis_mapper import upset_thread_item_to_redis_set
from src.mapper.upset_thread_mapper import set_to_upset_thread_item, redis_set_to_upset_thread_item
from logger import logging


logger = logging.getLogger(__name__)


events_redis_db = EventsRedisDb()
characters_redis_db = CharactersRedisDb()
event_sets_redis_db = EventSetsRedisDb()


def apply_filter(
        upset_factor,
        winner_initial_seed,
        loser_initial_seed,
        is_dq,
        min_upset_factor=-float('inf'),
        max_seed=float('inf'),
        include_dq=False,
):
    fulfills_min_upset_factor = upset_factor >= min_upset_factor
    fulfills_not_dq = not is_dq or include_dq
    fulfills_max_seed = any([winner_initial_seed <= max_seed, loser_initial_seed <= max_seed])
    return all([
        fulfills_min_upset_factor,
        fulfills_not_dq,
        fulfills_max_seed,
    ])


def get_upset_thread(sets):
    winners, losers, notables, dqs, other = [], [], [], [], []

    for s in sets:
        if s.is_winners_bracket() and apply_filter(
                s.upset_factor,
                s.winner.initial_seed,
                s.loser.initial_seed,
                s.is_dq(),
                min_upset_factor=1,
                max_seed=50,
        ):
            winners.append(s)
        elif not s.is_winners_bracket() and apply_filter(
                s.upset_factor,
                s.winner.initial_seed,
                s.loser.initial_seed,
                s.is_dq(),
                min_upset_factor=1,
                max_seed=50
        ):
            losers.append(s)
        elif s.is_dq_and_out() and apply_filter(
                s.upset_factor,
                s.winner.initial_seed,
                s.loser.initial_seed,
                is_dq=True,
                include_dq=True,
        ):
            dqs.append(s)
        elif s.is_notable() and apply_filter(
                -s.upset_factor,
                s.winner.initial_seed,
                s.loser.initial_seed,
                s.is_dq(),
                min_upset_factor=3,
                max_seed=50,
        ):
            notables.append(s)
        else:
            other.append(s)

    return UpsetThread(
        [set_to_upset_thread_item(s, 'winners') for s in winners],
        [set_to_upset_thread_item(s, 'losers') for s in losers],
        [set_to_upset_thread_item(s, 'notables') for s in sorted(notables, key=lambda x: x.upset_factor)],
        [set_to_upset_thread_item(s, 'dqs') for s in dqs],
        [set_to_upset_thread_item(s, 'other') for s in other],
    )


def get_character_name(character_key):
    if not characters_redis_db.is_characters_loaded():
        res = get_characters()
        characters_redis_db.add_characters(res['data']['videogame']['characters'])
        characters_redis_db.set_is_characters_loaded(1)
    return characters_redis_db.get_character_name(character_key)


def submit_to_subreddit(slug, subreddit_name, title, md):
    submission_id = events_redis_db.get_submission_id(slug)
    events_redis_db.set_last_updated_date(slug, int(time()))
    if submission_id:
        logger.info('Editing existing post')
        submission = reddit.submission(submission_id)
        submission.edit(md)
        return
    if not title:
        raise Exception("Title is required.")
    logger.info('Creating new post')
    subreddit = reddit.subreddit(subreddit_name)
    submission = subreddit.submit(title=title, selftext=md)
    events_redis_db.set_submission_id(slug, submission.id)
    events_redis_db.set_created_at(slug, int(time()))


def add_sets(slug, upset_thread):
    redis_set_mapping = {}
    for s in upset_thread.winners:
        redis_set_mapping[s.id] = upset_thread_item_to_redis_set(s, 'winners')
    for s in upset_thread.losers:
        redis_set_mapping[s.id] = upset_thread_item_to_redis_set(s, 'losers')
    for s in upset_thread.notables:
        redis_set_mapping[s.id] = upset_thread_item_to_redis_set(s, 'notables')
    for s in upset_thread.dqs:
        redis_set_mapping[s.id] = upset_thread_item_to_redis_set(s, 'dqs')
    for s in upset_thread.other:
        redis_set_mapping[s.id] = upset_thread_item_to_redis_set(s, 'other')
    event_sets_redis_db.add_sets(slug, redis_set_mapping)


def get_upset_thread_redis(slug):
    sets = event_sets_redis_db.get_sets(slug)
    winners, losers, notables, dqs, other = [], [], [], [], []
    for set_id, redis_set in sets.items():
        upset_thread_item = redis_set_to_upset_thread_item(int(set_id), redis_set)
        category = upset_thread_item.category
        if category == 'winners':
            winners.append(upset_thread_item)
        elif category == 'losers':
            losers.append(upset_thread_item)
        elif category == 'notables':
            notables.append(upset_thread_item)
        elif category == 'dqs':
            dqs.append(upset_thread_item)
        else:
            other.append(upset_thread_item)

    return UpsetThread(
        sorted(winners, key=lambda x: -x.upset_factor),
        sorted(losers, key=lambda x: -x.upset_factor),
        sorted(notables, key=lambda x: x.upset_factor),
        sorted(dqs, key=lambda x: -x.upset_factor),
        other,
    )
