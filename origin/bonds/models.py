import json
import logging
import traceback

from django.db import models
from djmoney.models.fields import CurrencyField

import requests

logger = logging.getLogger(__name__)


class Bond(models.Model):
    isin = models.CharField(max_length=250)
    size = models.BigIntegerField()
    currency = CurrencyField()
    maturity = models.DateField()
    lei = models.CharField(max_length=250)
    legal_name = models.CharField(max_length=250, null=True)

    def save(self, *args, **kwargs):
        # looks up legal name on GLEIF API
        url = 'https://leilookup.gleif.org/api/v2/leirecords?lei={}'.format(self.lei)
        try:
            response = requests.get(url)
        except requests.exceptions.BaseHTTPError:
            logger.error(traceback.format_exc())
        else:
            if response.status_code == 200:
                content = json.loads(response.content)
                legal_name = content[0]['Entity']['LegalName']['$']
                self.legal_name = legal_name
            else:
                logger.error('received status code {0} from GLEIF API for lei: {1}'.format(response.status_code,
                                                                                           self.lei))
        super(Bond, self).save(*args, **kwargs)
