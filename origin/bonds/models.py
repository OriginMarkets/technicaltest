from django.db import models

class PostBond(models.Model):
    isin = models.CharField(max_length=255)
    size = models.TextField()
    currency = models.TextField()
    maturity = models.DateTimeField()
    lei = models.TextField()