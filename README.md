# Origin

## API

We should be able to send a request to:

`POST /bonds/`

to create a "bond" with data that looks like:

```json
{
    "isin": "FR0000131104",
    "size": 100000000,
    "currency": "EUR",
    "maturity": "2025-02-28",
    "lei": "R0MUWSFPU8MPRO8K5P83"
}
```

We should be able to send a request to:

`GET /bonds/`

to see something like:

```json
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
```

## Features in development

* Token based authentication
* Filters
* Logging
* Throttling
* Pagination
* BDD testing
* Sphinx integration

## Workflow

### Linting

```bash
sh scripts/lint.sh
```

### Formatting

```bash
sh scripts/format.sh
```

### Testing

```bash
pytest
```

### Serving

```bash
sh scripts/dev.runserver.sh
```

For a clean database:

```bash
sh scripts/dev.runserver.sh -c
```

## Frontend

Small angular app:

* Conusmes the frontend

* Embeds the admin site

### Linting

```bash
grunt lint
```

### Formatting

```bash
grunt format
```

### Testing

```bash
grunt unitTests
grunt integrationTests
grunt e2eTests
```
### Running

```bash
grunt serveDev
```

## DevOps

### Building images

```bash
sh builder/prod.build.sh
```

### Deploying stacks

```bash
docker stack deploy prod -c prod.docker-compose.yml
```

### Terraform

```bash
terraform plan
terraform apply
```

### Ansible

```bash
ansible-playbook -i inventory/main.py playbooks/main.yml
```

### Naming conventions

Subprojects:

- origin

  - Django project

- origin-app
  
  - Angular app

- origin-ops
  
  - Dockerfiles
  - Ansible playbooks
  - Terraform configuration

### Author

- **Joel Lefkowitz** - _Initial work_ - [Joel Lefkowitz](https://github.com/JoelLefkowitz)
