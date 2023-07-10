from domain import Set, Entrant


def to_domain_set(s):
    entrants = [to_domain_entrant(slot) for slot in s['slots']]
    return Set(s['displayScore'], s['fullRoundText'], s['totalGames'], s['winnerId'], entrants)


def to_domain_entrant(slot):
    return Entrant(slot['entrant']['id'], slot['entrant']['name'], slot['entrant']['initialSeedNum'])
