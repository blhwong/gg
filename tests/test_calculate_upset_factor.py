from src.domain import upset_factor_table


def test_1():
    assert upset_factor_table.get_upset_factor(1, 1024) == -19


def test_2():
    assert upset_factor_table.get_upset_factor(251, 743) == -3


def test_3():
    assert upset_factor_table.get_upset_factor(17, 24) == 0
