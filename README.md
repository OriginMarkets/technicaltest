# Notes on the implementation

### Assumptions

- In a production system, validation would need to be specified precisely. As the spec did not specify anything about validation, some very loose assumptions have been made on the model level (though mostly the django defaults are used), but these are not tested as they are not actual system requirements.

- An assumption has been made that the user that creates a bond is the only user who can view that bond. This was done so as to fulfill the criterium of "each user will only see their own data".

- As the spec did not specify the need for a login page, this was not created. The admin login page can be used for now as a means of testing manually via the web browser. An admin user can be created with `./manage.py createsuperuser` to do this.

- An assumption was made that any errors coming from the GLEIF API (connection errors, unexpected json etc.) should bubble up as 500 errors in the REST endpoints as these are not the user's fault and therefore should not be 400 errors. This is what would happen by default, but in reality I would ask follow up questions to establish how this should be handled (should we save the legal name as empty string and log the error in the server logs? should we have strict lei identifier validation that doesn't allow a lei that the GLEIF API doesn't recognise?).


# Origin Markets Backend Test

### Spec:

We would like you to implement an api to: ingest some data representing bonds, query an external api for some additional data, store the result, and make the resulting data queryable via api.
- Fork this hello world repo leveraging Django & Django Rest Framework. (If you wish to use something else like flask that's fine too.)
- Please pick and use a form of authentication, so that each user will only see their own data. ([DRF Auth Options](https://www.django-rest-framework.org/api-guide/authentication/#api-reference))
- We are missing some data! Each bond will have a `lei` field (Legal Entity Identifier). Please use the [GLEIF API](https://www.gleif.org/en/lei-data/gleif-lei-look-up-api/access-the-api) to find the corresponding `Legal Name` of the entity which issued the bond.
- If you are using a database, SQLite is sufficient.
- Please test any additional logic you add.

#### Project Quickstart

Inside a virtual environment running Python 3:
- `pip install -r requirement.txt`
- `./manage.py runserver` to run server.
- `./manage.py test` to run tests.

#### API

We should be able to send a request to:

`POST /bonds/`

to create a "bond" with data that looks like:
~~~
{
    "isin": "FR0000131104",
    "size": 100000000,
    "currency": "EUR",
    "maturity": "2025-02-28",
    "lei": "R0MUWSFPU8MPRO8K5P83"
}
~~~
---
We should be able to send a request to:

`GET /bonds/`

to see something like:
~~~
[
    {
        "isin": "FR0000131104",
        "size": 100000000,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "R0MUWSFPU8MPRO8K5P83",
        "legal_name": "BNPPARIBAS"
    },
    ...
]
~~~
We would also like to be able to add a filter such as:
`GET /bonds/?legal_name=BNPPARIBAS`

to reduce down the results.
