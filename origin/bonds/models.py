from bonds.utils.currency import get_currency_choices
from bonds.utils.lei import get_legalname
from django.contrib.auth.models import User
from django.db import models


class Bond(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isin = models.CharField(unique=True, max_length=12)
    size = models.IntegerField()
    currency = models.CharField(max_length=3, choices=get_currency_choices())
    maturity = models.DateField()
    lei = models.CharField(max_length=20)
    legal_name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.legal_name = get_legalname(self.lei)
        super(Bond, self).save(*args, **kwargs)
