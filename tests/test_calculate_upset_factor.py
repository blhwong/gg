from src.service import calculate_upset_factor


def test_1():
    assert calculate_upset_factor(1, 1024) == -19


def test_2():
    assert calculate_upset_factor(251, 743) == -3


def test_3():
    assert calculate_upset_factor(17, 24) == 0
