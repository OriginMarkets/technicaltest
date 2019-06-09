from django.contrib import admin
from bonds.models import Bond

# Register your models here.

class BondAdmin(admin.ModelAdmin):
    list_display = ( 'isin', 'legal_name', 'size', 'currency', 'maturity', )
    exclude = ('user', )
    readonly_fields = ('legal_name',)

    # We are missing a select field with the currencies


admin.site.register(Bond, BondAdmin)
