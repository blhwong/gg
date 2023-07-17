from src.domain.upset_thread import UpsetThread


def test_upset_thread_1():
    winners = []
    losers = []
    notables = []
    dqs = []
    other = []

    ut = UpsetThread(winners, losers, notables, dqs, other)

    assert ut.winners is winners
    assert ut.losers is losers
    assert ut.notables is notables
    assert ut.dqs is dqs
    assert ut.other is other
