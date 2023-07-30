from time import time

from src.domain.set import Set, Entrant, Game, Selection, Character

e1 = Entrant(12394650, 'LG | Tweek', 3, 9, True)
e2 = Entrant(12687800, 'Zomba', 20, 8, False)
s1 = [Selection(e1, Character(1279, 'Diddy Kong')), Selection(e2, Character(1323, 'R.O.B.'))]
s2 = [Selection(e1, Character(1777, 'Sephiroth')), Selection(e2, Character(1323, 'R.O.B.'))]


def test_init_score_1():
    s = Set(
        "60482457",
        'Zomba 3 - LG | Tweek 0',
        None,
        5,
        -6,
        9,
        12687800,
        [e1, e2],
        None,
        int(time()),
    )
    assert s.score == '3-0'


def test_init_score_2():
    s = Set(
        "60482457",
        'Zomba 0 - LG | Tweek 3',
        None,
        5,
        -6,
        9,
        12687800,
        [e1, e2],
        None,
        int(time()),
    )
    assert s.score == '3-0'


def test_init_score_3():
    s = Set(
        "60482457",
        'Zomba 0 - LG | Tweek 3',
        None,
        5,
        -6,
        9,
        12687800,
        [e1, e2],
        [
            Game(16955184, 12687800, s1),
            Game(16955185, 12687800, s1),
            Game(16955186, 12687800, s2),
        ],
        int(time()),
    )
    assert s.score == '3-0'


def test_init_score_4():
    s = Set(
        "60482457",
        'Zomba 0 - LG | Tweek 3',
        None,
        5,
        -6,
        9,
        12687800,
        [e1, e2],
        [
            Game(16955184, 12687800, s1),
            Game(16955185, 12687800, s1),
            Game(16955186, 12394650, s2),
            Game(16955187, 12687800, s1),
        ],
        int(time()),
    )
    assert s.score == '3-1'


def test_init_score_5():
    s = Set(
        "60482457",
        'DQ',
        None,
        5,
        -6,
        9,
        12687800,
        [e1, e2],
        [
            Game(16955184, 12687800, s1),
            Game(16955185, 12687800, s1),
            Game(16955186, 12394650, s2),
            Game(16955187, 12687800, s1),
        ],
        int(time()),
    )
    assert s.score == 'DQ'


def test_init_score_6():
    s = Set(
        "60482457",
        'Zomba 1 - LG | Tweek 2',
        None,
        5,
        -6,
        9,
        12687800,
        [e1, e2],
        None,
        int(time()),
    )
    assert s.score == "2-1"


def test_init_score_7():
    s = Set(
        "60482457",
        'Zomba 0 - LG | Tweek 3',
        None,
        5,
        -6,
        9,
        12687800,
        [e1, e2],
        [
            Game(16955184, 12687800, s1),
            Game(16955185, 12687800, s1),
            Game(16955186, 12394650, s2),
        ],
        int(time()),
    )
    assert s.score == "3-0"


def test_get_winners_selection_1():
    s = Set(
        "60482457",
        'Zomba 0 - LG | Tweek 3',
        None,
        5,
        -6,
        9,
        12687800,
        [e1, e2],
        [
            Game(16955184, 12687800, s1),
            Game(16955185, 12687800, s1),
            Game(16955186, 12687800, s2),
        ],
        int(time()),
    )
    assert s.get_winner_character_selections() == 'R.O.B.'


def test_get_winners_selection_2():
    s = Set(
        "60482457",
        'Zomba 0 - LG | Tweek 3',
        None,
        5,
        -6,
        9,
        12687800,
        [e1, e2],
        [
            Game(16955184, 12687800, s1),
            Game(16955185, 12687800, s1),
            Game(16955186, 12687800, s2),
        ],
        int(time()),
    )
    assert s.get_loser_character_selections() == 'Diddy Kong, Sephiroth'


def test_get_characters_selections():
    s = Set(
        "60482457",
        'Zomba 0 - LG | Tweek 3',
        None,
        5,
        -6,
        9,
        12687800,
        [e1, e2],
        None,
        int(time()),
    )

    assert s.get_character_selections(12687800) == ''


def test_is_dq_and_out_1():
    s = Set(
        "60482457",
        'Zomba 0 - LG | Tweek 3',
        None,
        5,
        -6,
        9,
        12687800,
        [e1, e2],
        None,
        int(time()),
    )
    assert not s.is_dq_and_out()


def test_is_dq_and_out_2():
    s = Set(
        "60482457",
        'DQ',
        None,
        5,
        -6,
        9,
        12687800,
        [e1, e2],
        None,
        int(time()),
    )
    assert s.is_dq_and_out()


def test_is_notable_1():
    s = Set(
        "60482457",
        'Zomba 2 - LG | Tweek 3',
        None,
        5,
        -6,
        9,
        12687800,
        [e1, e2],
        None,
        int(time()),
    )
    assert s.is_notable()
