import json
from operator import itemgetter
from typing import List, Tuple


def get_currency_choices() -> List[Tuple]:
    """Get the list of currency tuples from the iso 4217 json file"""
    with open('origin/data/iso_4217.json', 'r') as f:
        currency_codes = json.load(f)

    # not isinstance(c['CcyNm'], dict) gets rid of the 'IsFund=True' entries
    choices = [(c['Ccy'], c['CcyNm']) for c in currency_codes['ISO_4217']['CcyTbl']['CcyNtry'] \
               if 'Ccy' in c.keys() and not isinstance(c['CcyNm'], dict)
               ]
    choices.sort(key=itemgetter(1))
    return choices

