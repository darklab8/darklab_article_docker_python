FROM python:3.10.5-slim-buster as base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /code

# curl for poetry setup
RUN apt update && apt install -y \ 
    curl \
    && rm -rf /var/lib/apt/lists/*


FROM base as dev
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
COPY pyproject.toml poetry.lock ./

RUN poetry config --local virtualenvs.create false
RUN poetry install --no-root

COPY pytest.ini ./
COPY src src
COPY utils utils

FROM dev as pre-prod
RUN poetry export --without-hashes --format=requirements.txt > requirements.txt
FROM python:3.10.5-slim-buster as prod

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /code

COPY --from=pre-prod /code/requirements.txt ./
RUN pip install -r requirements.txt

COPY pytest.ini ./
COPY src src
COPY utils utils
