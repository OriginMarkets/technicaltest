from operator import itemgetter
from .currency import get_currency_choices


def test_currency_choices():
    choices = get_currency_choices()

    assert len(choices) == 268
    assert choices[0] == ('XUA', 'ADB Unit of Account')
    assert choices[-1] == ('PLN', 'Zloty')
