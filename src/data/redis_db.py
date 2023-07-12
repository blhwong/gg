import redis


r = redis.Redis(decode_responses=True)


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
