from time import time
from src.domain.set import Set, Entrant, Game, Selection, Character
from src.domain.upset_thread import UpsetThread
from src.data.redis_mapper import upset_thread_item_to_redis_set
from src.mapper.upset_thread_mapper import set_to_upset_thread_item, redis_set_to_upset_thread_item
from logger import logging


logger = logging.getLogger(__name__)


class Service:

    def __init__(self, db_service, reddit_client, startgg_client):
        self.db_service = db_service
        self.reddit_client = reddit_client
        self.startgg_client = startgg_client

    @staticmethod
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

    def get_upset_thread(self, sets):
        winners, losers, notables, dqs, other = [], [], [], [], []

        for s in sets:
            if s.is_winners_bracket() and self.apply_filter(
                    s.upset_factor,
                    s.winner.initial_seed,
                    s.loser.initial_seed,
                    s.is_dq(),
                    min_upset_factor=1,
                    max_seed=50,
            ):
                winners.append(s)
            elif not s.is_winners_bracket() and self.apply_filter(
                    s.upset_factor,
                    s.winner.initial_seed,
                    s.loser.initial_seed,
                    s.is_dq(),
                    min_upset_factor=1,
                    max_seed=50
            ):
                losers.append(s)
            elif s.is_dq_and_out() and self.apply_filter(
                    s.upset_factor,
                    s.winner.initial_seed,
                    s.loser.initial_seed,
                    is_dq=True,
                    include_dq=True,
            ):
                dqs.append(s)
            elif s.is_notable() and self.apply_filter(
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

    def get_character_name(self, character_key):
        if not self.db_service.is_characters_loaded():
            res = self.startgg_client.get_characters()
            self.db_service.add_characters(res['data']['videogame']['characters'])
            self.db_service.set_is_characters_loaded(1)
        return self.db_service.get_character_name(character_key)

    def get_event(self, slug, page):
        return self.startgg_client.get_event(slug, page)

    def submit_to_subreddit(self, slug, subreddit_name, title, md):
        submission_id = self.db_service.get_submission_id(slug)
        self.db_service.set_last_updated_date(slug, int(time()))
        if submission_id:
            logger.info('Editing existing post')
            submission = self.reddit_client.submission(submission_id)
            submission.edit(md)
            return
        if not title:
            raise Exception("Title is required.")
        logger.info('Creating new post')
        subreddit = self.reddit_client.subreddit(subreddit_name)
        submission = subreddit.submit(title=title, selftext=md)
        self.db_service.set_submission_id(slug, submission.id)
        self.db_service.set_created_at(slug, int(time()))

    def add_sets(self, slug, upset_thread):
        redis_set_mapping = {}
        for s in upset_thread.winners:
            redis_set_mapping[s.id] = upset_thread_item_to_redis_set(s)
        for s in upset_thread.losers:
            redis_set_mapping[s.id] = upset_thread_item_to_redis_set(s)
        for s in upset_thread.notables:
            redis_set_mapping[s.id] = upset_thread_item_to_redis_set(s)
        for s in upset_thread.dqs:
            redis_set_mapping[s.id] = upset_thread_item_to_redis_set(s)
        for s in upset_thread.other:
            redis_set_mapping[s.id] = upset_thread_item_to_redis_set(s)
        self.db_service.add_sets(slug, redis_set_mapping)

    def get_upset_thread_db(self, slug):
        sets = self.db_service.get_sets(slug)
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

    def to_domain_set(self, s):
        entrants = [self.to_domain_entrant(slot['entrant']) for slot in s['slots']]
        winner_id = s['winnerId']
        l_placement = [entrant.placement for entrant in entrants if entrant.id != winner_id][0]
        games = None
        if s['games']:
            games = [self.to_domain_game(game) for game in s['games']]
        return Set(
            s['id'],
            s['displayScore'],
            s['fullRoundText'],
            s['totalGames'],
            s['round'],
            l_placement,
            winner_id,
            entrants,
            games,
            s['completedAt'],
        )

    @staticmethod
    def to_domain_entrant(entrant):
        return Entrant(
            entrant['id'],
            entrant['name'],
            entrant['initialSeedNum'],
            entrant['standing']['placement'],
            entrant['standing']['isFinal'],
        )

    def to_domain_game(self, game):
        selections = None
        if game['selections']:
            selections = [self.to_domain_selection(selection) for selection in game['selections']]
        return Game(
            game['id'],
            game['winnerId'],
            selections,
        )

    def to_domain_character(self, selection_type, value):
        if selection_type != "CHARACTER":
            return None
        return Character(value, self.get_character_name(value))

    def to_domain_selection(self, selection):
        return Selection(
            self.to_domain_entrant(selection['entrant']),
            self.to_domain_character(selection['selectionType'], selection['selectionValue']),
        )
