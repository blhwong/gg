from domain import Set, Entrant
import inflect

p = inflect.engine()


def to_domain_set(s):
    entrants = [to_domain_entrant(slot) for slot in s['slots']]
    return Set(
        s['id'],
        s['displayScore'],
        s['fullRoundText'],
        s['totalGames'],
        s['round'],
        s['lPlacement'],
        s['winnerId'],
        entrants,
    )


def to_domain_entrant(slot):
    return Entrant(
        slot['entrant']['id'],
        slot['entrant']['name'],
        slot['entrant']['initialSeedNum'],
    )


def to_line_item(s):
    text = f'{s.display_score} - Upset Factor {s.upset_factor}'
    if s.upset_factor >= 4:
        return f'**{text}**'
    return text


def to_loser_line_item(s):
    text = f'{s.display_score}, out at {p.ordinal(s.losers_placement)} - Upset Factor {s.upset_factor}'
    if s.upset_factor >= 4:
        return f'**{text}**'
    return text


def to_dq_line_item(s):
    return s.loser.name


def to_markdown(upset_thread):
    winners = '\\\n'.join([to_line_item(s) for s in upset_thread['winners']])
    losers = '\\\n'.join([to_loser_line_item(s) for s in upset_thread['losers']])
    notables = '\\\n'.join([to_line_item(s) for s in upset_thread['notables']])
    dqs = '\\\n'.join([to_dq_line_item(s) for s in upset_thread['dqs']])
    return f"""
# Winners:
{winners}

# Losers:
{losers}

# Notables:
{notables}

# DQs:
{dqs}
"""
