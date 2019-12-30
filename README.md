
# Locally (requires poetry)

```
    $ poetry install
    $ poetry shell
    $ python manage.py migrate
    $ python manage.py createsuperuser
    $ python manage.py runserver
```
Create user in localhost:8000/admin with your superuser account
make sure to give it permissions for bonds and legal entities.


# Docker:

To run app:
```shell
    $ docker-compose build
    $ docker-compose up -d app
    $ docker-compose exec app python manage.py migrate
    $ docker-compose exec app python manage.py createsuperuser
```


To run tests:
```shell
    $ docker-compose build
    $ docker-compose run --rm tests
```

To use the API here are some cURL commands:

# Plain virtualenv
```shell
    $ python -m venv env
    $ ./env/bin/activate
    $ pip install -r requirements.txt
    $ python manage.py migrate
    $ python manage.py createsuperuser
    $ python manage.py runserver
```

## Authenticate
```
curl -X POST -H "Content-Type: application/json" localhost:8000/api-token-auth/ -d '{"username": "", "password": ""}'
```

## Create a new Bond
```
curl \
    -X POST \
    -H "Authorization: Token xxx" \
    -H "Content-Type: application/json" \
    "localhost:8000/bonds" \
    -d '{"isin": "FR0000131104","size": 100000000,"currency": "EUR","maturity": "2025-02-28","lei": "R0MUWSFPU8MPRO8K5P83"}'
```

## List all Bonds for a User
```
curl \
    -X GET \
    -H "Authorization: Token xxx" \
    -H "Content-Type: application/json" \
    "localhost:8000/bonds"
```

## List all Bonds for a User filtered by lei
```
curl \
    -X GET \
    -H "Authorization: Token xxx" \
    -H "Content-Type: application/json" \
    "localhost:8000/bonds?lei=R0MUWSFPU8MPRO8K5P83"
```
