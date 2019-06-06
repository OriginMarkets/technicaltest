from unittest import TestCase, mock

import requests
import responses
from django.conf import settings
from django.test import SimpleTestCase
from parameterized import parameterized

from technicaltest.origin.bonds.logic import fetch_legal_entities_names, fetch_legal_entity_name

LEIS = ['261700K5E45DJCF5Z735', 'NKY7JRBKJHQQ68KJ6252']
LEIS_RESP_BODY = '[{"LEI":{"$":"261700K5E45DJCF5Z735"},"Entity":{"LegalName":{"@xml:lang":"EN","$":"APIR SYSTEMS LIMITED"},"LegalAddress":{"@xml:lang":"EN","FirstAddressLine":{"$":"Level 2, 33 Ainslee Place"},"City":{"$":"CANBERRA"},"Region":{"$":"AU-ACT"},"Country":{"$":"AU"},"PostalCode":{"$":"2601"}},"HeadquartersAddress":{"@xml:lang":"EN","FirstAddressLine":{"$":"Level 2, 33 Ainslee Place"},"City":{"$":"CANBERRA"},"Region":{"$":"AU-ACT"},"Country":{"$":"AU"},"PostalCode":{"$":"2601"}},"RegistrationAuthority":{"RegistrationAuthorityID":{"$":"RA000014"},"RegistrationAuthorityEntityID":{"$":"081 044 957"}},"LegalJurisdiction":{"$":"AU"},"LegalForm":{"EntityLegalFormCode":{"$":"R4KK"}},"EntityStatus":{"$":"ACTIVE"}},"Registration":{"InitialRegistrationDate":{"$":"2015-09-21T00:14:18+00:00"},"LastUpdateDate":{"$":"2019-06-03T09:42:47+00:00"},"RegistrationStatus":{"$":"ISSUED"},"NextRenewalDate":{"$":"2020-02-25T00:00:00+00:00"},"ManagingLOU":{"$":"529900T8BM49AURSDO55"},"ValidationSources":{"$":"FULLY_CORROBORATED"},"ValidationAuthority":{"ValidationAuthorityID":{"$":"RA000014"},"ValidationAuthorityEntityID":{"$":"081 044 957"}}}},{"LEI":{"$":"NKY7JRBKJHQQ68KJ6252"},"Entity":{"LegalName":{"$":"Global Macro Absolute Return Advantage Portfolio"},"OtherEntityNames":{"OtherEntityName":[{"@type":"PREVIOUS_LEGAL_NAME","$":"Global Strategies Portfolio"}]},"LegalAddress":{"FirstAddressLine":{"$":"Two International Place"},"City":{"$":"Boston"},"Region":{"$":"US-MA"},"Country":{"$":"US"},"PostalCode":{"$":"02110"}},"HeadquartersAddress":{"FirstAddressLine":{"$":"Two International Place"},"City":{"$":"Boston"},"Region":{"$":"US-MA"},"Country":{"$":"US"},"PostalCode":{"$":"02110"}},"RegistrationAuthority":{"RegistrationAuthorityID":{"$":"RA000613"},"RegistrationAuthorityEntityID":{"$":"001029754"}},"LegalJurisdiction":{"$":"US"},"EntityCategory":{"$":"FUND"},"LegalForm":{"EntityLegalFormCode":{"$":"9999"},"OtherLegalForm":{"$":"OTHER"}},"EntityStatus":{"$":"ACTIVE"}},"Registration":{"InitialRegistrationDate":{"$":"2012-06-28T09:07:00.000Z"},"LastUpdateDate":{"$":"2018-11-14T15:31:00.000Z"},"RegistrationStatus":{"$":"ISSUED"},"NextRenewalDate":{"$":"2019-09-27T20:07:00.000Z"},"ManagingLOU":{"$":"EVK05KS7XY1DEII3R011"},"ValidationSources":{"$":"FULLY_CORROBORATED"}}}]'


@mock.patch('technicaltest.origin.bonds.logic.LOG', mock.Mock())
class FetchLegalEntitiesNamesTestCase(TestCase):
    def _mock_request(self, body=LEIS_RESP_BODY, status=200):
        responses.add(
            responses.GET,
            settings.LEI_LOOKUP_URL,
            body=body,
            status=status
        )

    @responses.activate
    def test_fetch_legal_entities_names_success(self):
        self._mock_request()

        result = fetch_legal_entities_names(LEIS)

        self.assertEqual(len(responses.calls), 1)
        self.assertTrue(responses.calls[0].request.path_url.endswith('?lei=261700K5E45DJCF5Z735&lei=NKY7JRBKJHQQ68KJ6252'))
        self.assertDictEqual(
            result,
            {
                '261700K5E45DJCF5Z735': 'APIR SYSTEMS LIMITED',
                'NKY7JRBKJHQQ68KJ6252': 'Global Macro Absolute Return Advantage Portfolio'
            }
        )

    @parameterized.expand([
        ('connection', requests.ConnectionError),
        ('timeout', requests.Timeout),
        ('request', requests.RequestException),
    ])
    @responses.activate
    def test_fetch_legal_entities_names_error(self, _, exception_class):
        self._mock_request(body=exception_class())

        result = fetch_legal_entities_names(LEIS)

        self.assertIsNone(result)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_fetch_legal_entities_names_non_200_response(self):
        self._mock_request(status=401)

        result = fetch_legal_entities_names(LEIS)

        self.assertIsNone(result)
        self.assertEqual(len(responses.calls), 1)

    @parameterized.expand([
        ('invalid_json', 'fake_content'),
        ('missing_key', '[{"LEI":{"invalid_$":"261700K5E45DJCF5Z735"}}]')
    ])
    @responses.activate
    def test_fetch_legal_entities_names_malformed_body(self, _, body):
        self._mock_request(body=body)

        result = fetch_legal_entities_names(LEIS)

        self.assertIsNone(result)
        self.assertEqual(len(responses.calls), 1)


class FetchLegalEntityNameTestCase(SimpleTestCase):
    @mock.patch('technicaltest.origin.bonds.logic.fetch_legal_entities_names',
                mock.Mock(return_value={'261700K5E45DJCF5Z735': 'APIR SYSTEMS LIMITED'}))
    def test_fetch_legal_entity_name_success(self):
        self.assertEqual(
            fetch_legal_entity_name('261700K5E45DJCF5Z735'),
            'APIR SYSTEMS LIMITED'
        )

    @mock.patch('technicaltest.origin.bonds.logic.fetch_legal_entities_names', mock.Mock(return_value=None))
    def test_fetch_legal_entity_name_no_results(self):
        self.assertIsNone(fetch_legal_entity_name('261700K5E45DJCF5Z735'))
