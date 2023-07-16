from src.domain import Set, Entrant, Game, Selection, Character
from src.service import get_character_name


def to_domain_set(s):
    entrants = [to_domain_entrant(slot['entrant']) for slot in s['slots']]
    winner_id = s['winnerId']
    l_placement = [entrant.placement for entrant in entrants if entrant.id != winner_id][0]
    games = None
    if s['games']:
        games = [to_domain_game(game) for game in s['games']]
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


def to_domain_entrant(entrant):
    return Entrant(
        entrant['id'],
        entrant['name'],
        entrant['initialSeedNum'],
        entrant['standing']['placement'],
        entrant['standing']['is_final'],
    )


def to_domain_game(game):
    selections = None
    if game['selections']:
        selections = [to_domain_selection(selection) for selection in game['selections']]
    return Game(
        game['id'],
        game['winnerId'],
        selections,
    )


def to_domain_character(selectionType, value):
    if selectionType != "CHARACTER":
        return None
    return Character(value, get_character_name(value))


def to_domain_selection(selection):
    return Selection(
        to_domain_entrant(selection['entrant']),
        to_domain_character(selection['selectionType'], selection['selectionValue']),
    )
