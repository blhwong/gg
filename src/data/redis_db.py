from redis import Redis

from logger import logging

logger = logging.getLogger(__name__)


class RedisService:
    hash_key_prefix: str = "event"
    character_prefix: str = "character"
    is_character_loaded_key: str = "is_character_loaded"

    def __init__(self, r: Redis) -> None:
        self.r = r

    def is_characters_loaded(self) -> bool:
        return self.r.get(self.is_character_loaded_key) == "1"

    def set_is_characters_loaded(self, value: int) -> bool | None:
        return self.r.set(self.is_character_loaded_key, value)

    def add_characters(self, characters: list[dict[str, str]]) -> None:
        for character in characters:
            self.r.set(f"{self.character_prefix}:{character['id']}", character['name'])

    def get_character_name(self, character_key: int) -> str:
        return self.r.get(f"{self.character_prefix}:{character_key}")

    def get_last_updated_date(self, slug: str) -> str:
        return self.r.hget(f'{self.hash_key_prefix}:{slug}', "last_updated_date")

    def set_last_updated_date(self, slug: str, value: int) -> int:
        return self.r.hset(f'{self.hash_key_prefix}:{slug}', "last_updated_date", value)

    def set_created_at(self, slug: str, value: int) -> int:
        return self.r.hset(f'{self.hash_key_prefix}:{slug}', "created_at", value)

    def get_submission_id(self, slug: str) -> str:
        return self.r.hget(f'{self.hash_key_prefix}:{slug}', "submission_id")

    def set_submission_id(self, slug: str, value: str) -> int:
        return self.r.hset(f'{self.hash_key_prefix}:{slug}', "submission_id", value)

    @staticmethod
    def get_event_sets_key(slug: str) -> str:
        return f'event:{slug}_sets'

    def add_sets(self, slug: str, redis_set_mapping: dict[int, str]) -> None:
        for set_id, s in redis_set_mapping.items():
            self.add_set(slug, set_id, s)

    def add_set(self, slug: str, set_id: int, redis_set: str) -> None:
        logger.debug(f"add_set. slug={slug} set_id={set_id} redis_set={redis_set}")
        self.r.hset(self.get_event_sets_key(slug), set_id, redis_set)

    def get_sets(self, slug: str) -> dict[str, str]:
        return self.r.hgetall(self.get_event_sets_key(slug))
