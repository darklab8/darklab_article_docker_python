FROM python:3.10.5-slim-buster as base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /code

# gettext for `python3 manage.py compilemessages`
RUN apt update && apt install -y \ 
    gettext \
    && rm -rf /var/lib/apt/lists/*


FROM base as dev

ENV POETRY_HOME /opt/poetry
RUN python3 -m venv $POETRY_HOME
RUN $POETRY_HOME/bin/pip install poetry==1.2.2
ENV POETRY_BIN $POETRY_HOME/bin/poetry

COPY pyproject.toml poetry.lock ./

RUN $POETRY_BIN config --local virtualenvs.create false
RUN $POETRY_BIN install --no-root

COPY manage.py pytest.ini ./
COPY src src


FROM dev as pre-prod
RUN $POETRY_BIN export --without-hashes --format=requirements.txt > requirements.txt
FROM python:3.10.5-slim-buster as prod

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /code

COPY --from=pre-prod /code/requirements.txt ./
RUN pip install -r requirements.txt

COPY manage.py pytest.ini ./
COPY src src

# run if project has translations
# RUN ./manage.py compilemessages

# gathering statics if django admin is used
RUN ./manage.py collectstatic --noinput --clear