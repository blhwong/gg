from logger import logging

logger = logging.getLogger(__name__)


class RedisService:
    hash_key_prefix = "event"
    character_prefix = "character"
    is_character_loaded_key = "is_character_loaded"

    def __init__(self, r):
        self.r = r

    def is_characters_loaded(self):
        return self.r.get(self.is_character_loaded_key) == "1"

    def set_is_characters_loaded(self, value):
        return self.r.set(self.is_character_loaded_key, value)

    def add_characters(self, characters):
        for character in characters:
            self.r.set(f"{self.character_prefix}:{character['id']}", character['name'])

    def get_character_name(self, character_key):
        return self.r.get(f"{self.character_prefix}:{character_key}")

    def get_last_updated_date(self, slug):
        return self.r.hget(f'{self.hash_key_prefix}:{slug}', "last_updated_date")

    def set_last_updated_date(self, slug, value):
        return self.r.hset(f'{self.hash_key_prefix}:{slug}', "last_updated_date", value)

    def set_created_at(self, slug, value):
        return self.r.hset(f'{self.hash_key_prefix}:{slug}', "created_at", value)

    def get_submission_id(self, slug):
        return self.r.hget(f'{self.hash_key_prefix}:{slug}', "submission_id")

    def set_submission_id(self, slug, value):
        return self.r.hset(f'{self.hash_key_prefix}:{slug}', "submission_id", value)

    @staticmethod
    def get_event_sets_key(slug):
        return f'event:{slug}_sets'

    def add_sets(self, slug, redis_set_mapping):
        for set_id, s in redis_set_mapping.items():
            self.add_set(slug, set_id, s)

    def add_set(self, slug, set_id, redis_set):
        logger.debug(f"add_set. slug={slug} set_id={set_id} redis_set={redis_set}")
        self.r.hset(self.get_event_sets_key(slug), set_id, redis_set)

    def get_sets(self, slug):
        return self.r.hgetall(self.get_event_sets_key(slug))
