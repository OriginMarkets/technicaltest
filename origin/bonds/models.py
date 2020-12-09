from django.db.models import CharField, DateTimeField, Model, DecimalField, DateField, ForeignKey, CASCADE
from django.conf import settings
from babel import numbers


class Bond(Model):
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="bonds",
        on_delete=CASCADE,
    )
    
    created = DateTimeField(auto_now_add=True)

    # Bond ISIN Code
    # Example: FR0000131104
    # 12 character code
    # https://www.isin.net/bond-isin-code/
    isin = CharField(max_length=12)

    # Bond size
    # Example: 100000000
    # For a whole number we could use size = IntegerField() however
    # it's sensible to use two decimal places here
    size = DecimalField(max_digits=15, decimal_places=2)

    # Currency code
    # Example: EUR
    # 3 character string
    # For now this can be implemented as a character field
    # To allow more flexability we can use py-moneyed in the future
    currency = CharField(max_length=3)

    # Example: 2025-02-28
    # yyyy-mm-dd date string
    maturity = DateField()

    # LEI
    # Example: R0MUWSFPU8MPRO8K5P83
    # 20 character identifier
    # https://www.bourse.lu/lei
    lei = CharField(max_length=20)

    # Legal Name
    # Exmple: BNPPARIBAS
    # Example2: Société Générale Effekten GmbH
    # Set null=True to allow POST requests to omit this field
    legal_name = CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Bond with LEI: {self.lei}"

    def formatted_size(self):
        return numbers.format_currency(self.size, self.currency)

    class Meta:
        ordering = ["created"]
