import datetime
import factory
import random
from django.contrib.auth.models import User, Group

from .models import Bond

LEI_SAMPLES = {
    '21380016UZS36PC85Y22': 'ORIGIN GROUP LIMITED',
    '894500TFYBOUIM1WUN34': 'DEUTSCH-BELGISCH-LUXEMBURGISCHE HANDELSKAMER - BELGISCH-LUXEMBURGS-DUITSE KAMER VAN KOOPHANDEL - CHAMBRE DE COMMERCE BELGO-LUXEMBOURGEOISE-ALLEMANDE'
}


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'john{n}')
    email = factory.Sequence(lambda n: f'lennon{n}@thebeatles.com')
    password = factory.PostGenerationMethodCall(
        'set_password', 'johnpassword'
    )


class BondFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bond

    isin = factory.Sequence(lambda n: f'ISIN{n}')
    size = random.randint(1, 10000)
    currency = 'EUR'
    maturity = datetime.date.today()
    lei = random.choice(list(LEI_SAMPLES.keys()))

    user = factory.SubFactory(UserFactory)
