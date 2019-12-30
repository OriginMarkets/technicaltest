API_DATA = [
    {
        "LEI": {"$": "R0MUWSFPU8MPRO8K5P83"},
        "Entity": {
            "LegalName": {"@xml:lang": "fr", "$": "BNP PARIBAS"},
            "TransliteratedOtherEntityNames": {
                "TransliteratedOtherEntityName": [
                    {
                        "@type": "AUTO_ASCII_TRANSLITERATED_LEGAL_NAME",
                        "@xml:lang": "fr",
                        "$": "BNP PARIBAS",
                    }
                ]
            },
            "LegalAddress": {
                "@xml:lang": "fr",
                "FirstAddressLine": {"$": "16 BD DES ITALIENS"},
                "City": {"$": "PARIS 9"},
                "Country": {"$": "FR"},
                "PostalCode": {"$": "75009"},
            },
            "HeadquartersAddress": {
                "@xml:lang": "fr",
                "FirstAddressLine": {"$": "16 BD DES ITALIENS"},
                "City": {"$": "PARIS 9"},
                "Country": {"$": "FR"},
                "PostalCode": {"$": "75009"},
            },
            "RegistrationAuthority": {
                "RegistrationAuthorityID": {"$": "RA000189"},
                "RegistrationAuthorityEntityID": {"$": "662042449"},
            },
            "LegalJurisdiction": {"$": "FR"},
            "LegalForm": {"EntityLegalFormCode": {"$": "K65D"}},
            "EntityStatus": {"$": "ACTIVE"},
        },
        "Registration": {
            "InitialRegistrationDate": {"$": "2012-12-31T00:00:00.000+01:00"},
            "LastUpdateDate": {"$": "2019-12-19T22:03:32.003+01:00"},
            "RegistrationStatus": {"$": "ISSUED"},
            "NextRenewalDate": {"$": "2020-02-07T00:00:00.000+01:00"},
            "ManagingLOU": {"$": "969500Q2MA9VBQ8BG884"},
            "ValidationSources": {"$": "FULLY_CORROBORATED"},
            "ValidationAuthority": {
                "ValidationAuthorityID": {"$": "RA000189"},
                "ValidationAuthorityEntityID": {"$": "662042449"},
            },
        },
        "Extension": {
            "leifr:SIREN": {"$": "662042449"},
            "leifr:EconomicActivity": {
                "leifr:NACEClassCode": {"$": "64.19"},
                "leifr:SousClasseNAF": {"$": "64.19Z"},
            },
            "leifr:LegalFormCodification": {
                "@uri": "http:\/\/id.insee.fr\/codes\/cj\/n2",
                "$": "55",
            },
        },
    }
]
