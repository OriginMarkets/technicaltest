from django.db import models


class Bond(models.Model):
    isin = models.CharField(max_length=12)
    size = models.IntegerField()
    currency = models.CharField(max_length=3)
    maturity = models.DateField()
    lei = models.CharField(max_length=20)
    # NOTE: Not enough is known about the validation expectations for legal
    # name. Possibly should not be set to blank=True at model level but
    # at serializer level (the user should not have to supply it
    # since it is taken from the GLEIF API)
    legal_name = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
