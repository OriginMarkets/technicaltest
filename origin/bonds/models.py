import re
from iso4217 import Currency
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from pygleif import GLEIF
from urllib.error import HTTPError

currency_choices_map = { e.code: e.code for e in list(Currency) }

class IsinValidator(object):
    """
        Validates ISIN numbers
    """

    # Simple regex validator
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


class SizeValidator(object):
    """
        Validates size numbers to ensure positivity
    """

    def validate(size):
        if size < 0:
            raise ValidationError('size must not be negative'.format(size))


class Bond(models.Model):
    # Keep track of unmodifiable fields
    readonly_fields = ('legal_name',)

    def __init__(self, *args, **kwargs):
        super(Bond, self).__init__(*args, **kwargs)

        # Store lei and legal_name for to detect changes on the model
        self._original_lei = self.lei
        self._original_legal_name = self.legal_name

    def populate_legal_name(self):
        """
        Using the GLEIF library we can easily retrieve the legal name, though
        the pypi package is outdated the repo is current at the time of writing

        * NOTE The exceptions GLEIF raises are not so standard
        """
        try:
            self.legal_name = GLEIF(self.lei).entity.legal_name
        except IndexError:
            # GLEIF will return this when the LEI is not found
            raise ValidationError("Not existent LEI")
        except HTTPError:
            raise ValidationError("Invalid LEI or GLEIF Lookup API not available")

    def save(self, *args, **kwargs):
        """
        Override the save method to be able to validate without repeating yourself
        on the handlers
        """
        self.legal_name = self._original_legal_name
        if not self.legal_name or self._original_lei != self.lei:
            self.populate_legal_name()
        self.full_clean()
        super(Bond, self).save(*args, **kwargs)

    # Fields for the model
    isin = models.CharField(max_length=12, primary_key=True, validators=[IsinValidator.validate])
    size = models.IntegerField(validators=[SizeValidator.validate])
    currency = models.CharField(max_length=3, choices=list(currency_choices_map.items()), validators=[CurrencyValidator.validate])
    maturity = models.DateField()
    lei = models.CharField(max_length=20, validators=[LeiValidator.validate])
    legal_name = models.CharField(max_length=256)
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
