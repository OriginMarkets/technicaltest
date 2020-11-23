from django.contrib import admin
from .models import Bonds

# Register your models here.
class BondsAdmin(admin.ModelAdmin):
    list_display = ['isin', 'size', 'currency', 'maturity', 'lei', 'legal_name']


admin.site.register(Bonds, BondsAdmin)