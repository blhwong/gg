from datetime import datetime

import inflect
from pytz import timezone, utc

from src.domain.upset_thread import UpsetThread, UpsetThreadItem

p = inflect.engine()

DATETIME_FORMAT = '%m/%d/%y %I:%M %p %Z'


def to_line_item(item: UpsetThreadItem) -> str:
    words = [item.winners_name]
    if item.winners_characters:
        words.append(f'({item.winners_characters})')
    words.append(f'(seed {item.winners_seed})')
    words.append(item.score)
    words.append(item.losers_name)
    if item.losers_characters:
        words.append(f'({item.losers_characters})')
    losers_seed = f'(seed {item.losers_seed})'
    if item.is_winners_bracket:
        words.append(losers_seed)
    else:
        words.append(f'{losers_seed}, out at {p.ordinal(item.losers_placement)}')
    if item.upset_factor > 0:
        words.append(f'- Upset Factor {item.upset_factor}')

    text = ' '.join(words)
    if item.upset_factor >= 4:
        return f'**{text}**'
    return text


def to_dq_line_item(item: UpsetThreadItem) -> str:
    return item.losers_name


def to_markdown(upset_thread: UpsetThread, slug: str) -> str:
    winners = '  \n'.join([to_line_item(s) for s in upset_thread.winners])
    losers = '  \n'.join([to_line_item(s) for s in upset_thread.losers])
    notables = '  \n'.join([to_line_item(s) for s in upset_thread.notables])
    dqs = '  \n'.join([to_dq_line_item(s) for s in upset_thread.dqs])
    t = datetime.now(tz=utc)
    t = t.astimezone(timezone('US/Pacific'))
    t = t.strftime(DATETIME_FORMAT)
    return f"""[Bracket](https://start.gg/{slug})
    
# Winners
{winners}

# Losers
{losers}

# Notables
{notables}

# DQs
{dqs}

*Last updated at: {t}*
"""
