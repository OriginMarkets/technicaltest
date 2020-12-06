from bonds.factories import LEI_SAMPLES
from .currency import get_currency_choices
from .lei import get_legalname


def test_currency_choices():
    choices = get_currency_choices()

    assert len(choices) == 268
    assert choices[0] == ('XUA', 'ADB Unit of Account')
    assert choices[-1] == ('PLN', 'Zloty')


def test_lei_get_legalname():
    for lei, legalname in LEI_SAMPLES.items():
        result = get_legalname(lei)
        assert result == legalname
