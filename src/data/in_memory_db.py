from src.integrations.startgg.api import get_characters


class SetsInMemoryDb:

    def __init__(self):
        self.storage = {}

    def add_sets(self, sets):
        for s in sets:
            self.storage[s.id] = s

    def get_sets(self):
        return self.storage.values()


class CharactersInMemoryDb:

    def __init__(self):
        self.storage = {}
        res = get_characters()
        self.add_characters(res['data']['videogame']['characters'])

    def add_characters(self, characters):
        for character in characters:
            self.storage[character['id']] = character['name']

    def get_character_name(self, value):
        return self.storage[value]
