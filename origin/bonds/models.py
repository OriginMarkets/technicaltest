from django.db import models


class Bonds(models.Model):
    isin = models.CharField(max_length=12, primary_key=True)
    size = models.PositiveIntegerField(null=False, blank=False)
    currency = models.CharField(max_length=6, null=False, blank=False)
    maturity = models.DateField(auto_now=False, auto_now_add=False, null=False, blank=False)
    # check max_length of lei API
    lei = models.CharField(max_length=20, null=False, blank=False)
    legal_name = models.CharField(max_length=30, null=True, blank=True)
