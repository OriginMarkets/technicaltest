from enum import Enum

from django.conf import settings
from django.db import models


# TODO move this to common package, it's not bond specific in any way
# I should not leave a comment like this for future as it will likely be ignored, forgotten
# but this will not be worked on any further
class CURRENCIES(Enum):
    EUR = 'EUR'
    GBP = 'GBP'


# this is likely not bond specific as well
class LegalEntity(models.Model):
    # Legal Entity Identifier
    lei = models.CharField(max_length=50, blank=False, null=False, unique=True)
    legal_name = models.CharField(max_length=200, blank=True, null=True)

    # TODO should have at least some auto timestamps on models to track changes, I would use some common model, internal
    # or from a 3rd party lib but not gonna bother here as it's of no importance for test case
    # tracking who changed a record could be a must if records can be updated not only by owner(user/customer)
    # created
    # updated


class Bond(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.PROTECT)
    legal_entity = models.ForeignKey(LegalEntity, blank=False, null=False, on_delete=models.PROTECT)
    isin = models.CharField(max_length=50, blank=False, null=False)
    size = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=False)
    currency = models.CharField(max_length=3, blank=False, null=False,
                                choices=[(currency.name, currency.value) for currency in CURRENCIES])
    maturity = models.DateField(blank=False, null=False)

    # TODO should have at least some auto timestamps on models to track changes, I would use some common model, internal
    # or from a 3rd party lib but not gonna bother here as it's of no importance for test case
    # tracking who changed a record could be a must if records can be updated not only by owner(user/customer)
    # created
    # updated
