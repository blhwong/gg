import redis


r = redis.Redis(decode_responses=True)


class AppStateRedisDb:

    hash_key = "appstate"

    def is_characters_loaded(self):
        return r.hget(self.hash_key, "is_character_loaded")

    def set_is_character_loaded(self, value):
        return r.hset(self.hash_key, "is_character_loaded", value)

    def get_submission_id(self):
        return r.hget(self.hash_key, "submission_id")

    def set_submission_id(self, value):
        return r.hset(self.hash_key, "submission_id", value)


class CharactersRedisDb:

    prefix = "character"

    def add_characters(self, characters):
        for character in characters:
            print(character['id'])
            r.set(f"{self.prefix}:{character['id']}", character['name'])

    def get_character_name(self, character_key):
        return r.get(f"{self.prefix}:{character_key}")
