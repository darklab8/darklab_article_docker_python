FROM python:3.10.5-slim-buster as base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /code


FROM base as dep-poetry
RUN apt update && apt install -y \ 
    curl \
    && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
COPY pyproject.toml poetry.lock ./
RUN poetry config --local virtualenvs.create false
RUN poetry install --no-root
COPY src src


FROM base as dep-pipenv
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system
COPY src src


FROM base as dep-pip
COPY requirements.txt constraints.txt ./
RUN pip install -r requirements.txt -c constraints.txt
COPY src src