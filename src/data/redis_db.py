import redis
import settings

r = redis.Redis(
    decode_responses=True,
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)


class CharactersRedisDb:

    prefix = "character"
    is_character_loaded_key = "is_character_loaded"

    def is_characters_loaded(self):
        return r.get(self.is_character_loaded_key) == "1"

    def set_is_characters_loaded(self, value):
        return r.set(self.is_character_loaded_key, value)

    def add_characters(self, characters):
        for character in characters:
            r.set(f"{self.prefix}:{character['id']}", character['name'])

    def get_character_name(self, character_key):
        return r.get(f"{self.prefix}:{character_key}")


class EventsRedisDb:

    hash_key_prefix = "event"

    def get_last_updated_date(self, slug):
        return r.hget(f'{self.hash_key_prefix}:{slug}', "last_updated_date")

    def set_last_updated_date(self, slug, value):
        return r.hset(f'{self.hash_key_prefix}:{slug}', "last_updated_date", value)

    def set_created_at(self, slug, value):
        return r.hset(f'{self.hash_key_prefix}:{slug}', "created_at", value)

    def get_submission_id(self, slug):
        return r.hget(f'{self.hash_key_prefix}:{slug}', "submission_id")

    def set_submission_id(self, slug, value):
        return r.hset(f'{self.hash_key_prefix}:{slug}', "submission_id", value)


class EventSetsRedisDb:

    @staticmethod
    def get_key(slug):
        return f'event:{slug}_sets'

    def add_sets(self, slug, redis_set_mapping):
        for set_id, s in redis_set_mapping.items():
            self.add_set(slug, set_id, s)

    def add_set(self, slug, set_id, redis_set):
        r.hset(self.get_key(slug), set_id, redis_set)

    def get_sets(self, slug):
        return r.hgetall(self.get_key(slug))
