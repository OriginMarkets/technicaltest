from .currency import get_currency_choices
from .lei import get_legalname


def test_currency_choices():
    choices = get_currency_choices()

    assert len(choices) == 268
    assert choices[0] == ('XUA', 'ADB Unit of Account')
    assert choices[-1] == ('PLN', 'Zloty')


def test_lei_get_legalname():
    result = get_legalname('21380016UZS36PC85Y22')
    assert result == 'ORIGIN GROUP LIMITED'
    result = get_legalname('894500TFYBOUIM1WUN34')
    assert result == 'DEUTSCH-BELGISCH-LUXEMBURGISCHE HANDELSKAMER - BELGISCH-LUXEMBURGS-DUITSE KAMER VAN KOOPHANDEL - CHAMBRE DE COMMERCE BELGO-LUXEMBOURGEOISE-ALLEMANDE'
