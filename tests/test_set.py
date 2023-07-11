from src.domain import Set, Entrant, Game, Selection, Character


e1 = Entrant(12394650, 'LG | Tweek', 3)
e2 = Entrant(12687800, 'Zomba', 20)
s1 = [Selection(e1, Character(1279, 'Diddy Kong')), Selection(e2, Character(1323, 'R.O.B.'))]
s2 = [Selection(e1, Character(1777, 'Sephiroth')), Selection(e2, Character(1323, 'R.O.B.'))]


def test_init_score_1():
    s = Set(
        60482457,
        'Zomba 3 - LG | Tweek 0',
        None,
        3,
        -6,
        9,
        12687800,
        [e1, e2],
        None,
    )
    assert s.score == '3-0'


def test_init_score_2():
    s = Set(
        60482457,
        'Zomba 0 - LG | Tweek 3',
        None,
        3,
        -6,
        9,
        12687800,
        [e1, e2],
        None,
    )
    assert s.score == '3-0'


def test_init_score_3():
    s = Set(
        60482457,
        'Zomba 0 - LG | Tweek 3',
        None,
        3,
        -6,
        9,
        12687800,
        [e1, e2],
        [
            Game(16955184, 12687800, s1),
            Game(16955185, 12687800, s1),
            Game(16955186, 12687800, s2),
        ],
    )
    assert s.score == '3-0'


def test_get_winners_selection_1():
    s = Set(
        60482457,
        'Zomba 0 - LG | Tweek 3',
        None,
        3,
        -6,
        9,
        12687800,
        [e1, e2],
        [
            Game(16955184, 12687800, s1),
            Game(16955185, 12687800, s1),
            Game(16955186, 12687800, s2),
        ],
    )
    assert s.get_winner_character_selections() == 'R.O.B.'


def test_get_winners_selection_2():
    s = Set(
        60482457,
        'Zomba 0 - LG | Tweek 3',
        None,
        3,
        -6,
        9,
        12687800,
        [e1, e2],
        [
            Game(16955184, 12687800, s1),
            Game(16955185, 12687800, s1),
            Game(16955186, 12687800, s2),
        ],
    )
    assert s.get_loser_character_selections() == 'Diddy Kong, Sephiroth'


def test_get_characters_selections():
    s = Set(
        60482457,
        'Zomba 0 - LG | Tweek 3',
        None,
        3,
        -6,
        9,
        12687800,
        [e1, e2],
        None,
    )

    assert s.get_character_selections(12687800) == ''
