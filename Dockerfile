FROM python:3.7-slim

ARG ENV
ENV POETRY_VERSION=1.0.0 \
    ENV=${ENV:-development} \
    BUILD_DEPS="curl" \
    PACKAGES="postgresql-client"


WORKDIR /app

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && \
    poetry install $(test "${ENV}" == production && echo "--no-dev") --no-interaction --no-ansi && \
    apt-get update && apt-get install -y -qq --no-install-recommends ${BUILD_DEPS} ${PACKAGES} && \
    curl https://raw.githubusercontent.com/kadwanev/retry/1.0.1/retry -o /usr/local/bin/retry && \
    chmod +x /usr/local/bin/retry && \
    apt-get autoremove -y ${BUILD_DEPS} && \
    rm -rf /root/.cache

COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]
