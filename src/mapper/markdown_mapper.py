import inflect
from datetime import datetime
from pytz import timezone, utc

p = inflect.engine()


DATETIME_FORMAT = '%m/%d/%y %I:%M %p %Z'


def to_line_item(item):
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


def to_dq_line_item(item):
    return item.losers_name


def to_markdown(upset_thread):
    winners = '  \n'.join([to_line_item(s) for s in upset_thread.winners])
    losers = '  \n'.join([to_line_item(s) for s in upset_thread.losers])
    notables = '  \n'.join([to_line_item(s) for s in upset_thread.notables])
    dqs = '  \n'.join([to_dq_line_item(s) for s in upset_thread.dqs])
    t = datetime.now(tz=utc)
    t = t.astimezone(timezone('US/Pacific'))
    t = t.strftime(DATETIME_FORMAT)
    return f"""
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
