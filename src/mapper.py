from domain import Set, Entrant, Game, Selection, Character
from src.data.db import CharactersInMemoryDb
import inflect

p = inflect.engine()

characters_db = CharactersInMemoryDb()


def to_domain_set(s):
    entrants = [to_domain_entrant(slot['entrant']) for slot in s['slots']]
    games = None
    if s['games']:
        games = [to_domain_game(game) for game in s['games']]
    return Set(
        s['id'],
        s['displayScore'],
        s['fullRoundText'],
        s['totalGames'],
        s['round'],
        s['lPlacement'],
        s['winnerId'],
        entrants,
        games,
    )


def to_domain_entrant(entrant):
    return Entrant(
        entrant['id'],
        entrant['name'],
        entrant['initialSeedNum'],
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
    return Character(value, characters_db.get_character_name(value))


def to_domain_selection(selection):
    return Selection(
        to_domain_entrant(selection['entrant']),
        to_domain_character(selection['selectionType'], selection['selectionValue'])

    )


def to_line_item(s):
    winners_characters, losers_characters = s.get_winner_character_selections(), s.get_loser_character_selections()
    words = [s.winner.name]
    if winners_characters:
        words.append(f'({winners_characters})')
    words.append(f'(seed {s.winner.initial_seed})')
    words.append(s.score)
    words.append(s.loser.name)
    if losers_characters:
        words.append(f'({losers_characters})')
    losers_seed = f'(seed {s.loser.initial_seed})'
    if s.is_winners_bracket():
        words.append(losers_seed)
    else:
        words.append(f'{losers_seed}, out at {p.ordinal(s.losers_placement)}')
    if s.upset_factor > 0:
        words.append(f'- Upset Factor {s.upset_factor}')

    text = ' '.join(words)
    if s.upset_factor >= 4:
        return f'**{text}**'
    return text


def to_table_line_item(s, is_include_upset_factor=True):
    winners_characters, losers_characters = s.get_winner_character_selections(), s.get_loser_character_selections()
    winner_name = s.winner.name.replace('|', '\|')
    winner = [f'{winner_name}']
    if winners_characters:
        winner.append(f'({winners_characters})')
    winner.append(f'(seed {s.winner.initial_seed})')

    loser_name = s.loser.name.replace('|', '\|')
    loser = [f'{loser_name}']
    if losers_characters:
        loser.append(f'({losers_characters})')
    if not s.is_winners_bracket():
        loser.append(f'(seed {s.loser.initial_seed}), out at {p.ordinal(s.losers_placement)}')
    else:
        loser.append(f'(seed {s.loser.initial_seed})')
    score = s.score
    upset_factor = f'Upset Factor {s.upset_factor}'

    columns = [' '.join(winner), score, ' '.join(loser)]
    if is_include_upset_factor:
        columns.append(str(upset_factor))

    if s.upset_factor >= 4:
        return f"|**{'**|**'.join(columns)}**|"

    return f"|{'|'.join(columns)}|"


def to_dq_line_item(s):
    return s.loser.name


def to_markdown(upset_thread):
    winners = '  \n'.join([to_line_item(s) for s in upset_thread.winners])
    losers = '  \n'.join([to_line_item(s) for s in upset_thread.losers])
    notables = '  \n'.join([to_line_item(s) for s in upset_thread.notables])
    dqs = '  \n'.join([to_dq_line_item(s) for s in upset_thread.dqs])
    return f"""
# Winners
{winners}

# Losers
{losers}

# Notables
{notables}

# DQs
{dqs}
"""


def to_markdown_table(upset_thread):
    winners = '\n'.join([to_table_line_item(s) for s in upset_thread.winners])
    losers = '\n'.join([to_table_line_item(s) for s in upset_thread.losers])
    notables = '\n'.join([to_table_line_item(s, is_include_upset_factor=False) for s in upset_thread.notables])
    dqs = '  \n'.join([to_dq_line_item(s) for s in upset_thread.dqs])
    return f"""
# Winners
|  |  |  |  |
|------|:-----:|----------|:-------:|
{winners}

# Losers
|  |  |  |  |
|------|:-----:|----------|:--------:|
{losers}

# Notables
|  |  |  |
|------|:-----:|----------|
{notables}

# DQs
{dqs}
"""
