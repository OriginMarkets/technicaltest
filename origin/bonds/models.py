from django.db import models
from django.contrib.auth.models import User


class Bond(models.Model):
    isin = models.CharField(max_length=12)
    size = models.PositiveIntegerField(null=True, blank=False)
    currency = models.CharField(max_length=6, null=True, blank=False)
    maturity = models.DateField(null=True) #auto_now=False, auto_now_add=False, null=False, blank=False)
    lei = models.CharField(max_length=20, null=True, blank=False)
    legal_name = models.CharField(max_length=30, null=True, blank=True)
    owner = models.ForeignKey(User, related_name="bonds", on_delete=models.CASCADE, null=True)

   
