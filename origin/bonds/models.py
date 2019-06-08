import re
from iso4217 import Currency
from django.db import models
from django.core.exceptions import ValidationError
from pygleif import GLEIF


class IsinValidator(object):
    """
        Validates ISIN numbers
    """
    validator = re.compile(r"^[A-Z]{2}[A-Z0-9]{9}[0-9]")

    @classmethod
    def validate(cls, isin):
        if not cls.validator.match(isin):
            raise ValidationError('{} is an invalid ISIN'.format(isin))


class CurrencyValidator(object):
    """
        Validates currency codes using the iso4217 list
    """
    def validate(currency):
        if not getattr(Currency, currency.lower(), False):
            raise ValidationError('{} does not exist in iso4217'.format(currency))


class LeiValidator(object):
    """
        Validates LEI numbers
    """

    def validate(lei):
        if not (len(lei) == 20 and lei.isalnum()):
            raise ValidationError('{} is an invalid LEI'.format(lei))


class Bond(models.Model):
    readonly_fields = ('legal_name',)

    def __init__(self, *args, **kwargs):
        super(Bond, self).__init__(*args, **kwargs)
        self._original_lei = self.lei
        self._original_legal_name = self.legal_name

    def populate_legal_name(self):
        try:
            self.legal_name = GLEIF(self.lei).entity.legal_name
        except IndexError:
            # GLEIF will return this when the LEI is not found
            raise ValidationError("Not existent LEI")

    def save(self, *args, **kwargs):
        print(self.legal_name)
        self.legal_name = self._original_legal_name
        if not self.legal_name or self._original_lei != self.lei:
            self.populate_legal_name()
        self.full_clean()
        super(Bond, self).save(*args, **kwargs)

    isin = models.CharField(max_length=12, primary_key=True, validators=[IsinValidator.validate])
    size = models.IntegerField()
    currency = models.CharField(max_length=3, validators=[CurrencyValidator.validate])
    maturity = models.DateField()
    lei = models.CharField(max_length=20, validators=[LeiValidator.validate])
    legal_name = models.CharField(max_length=256)
