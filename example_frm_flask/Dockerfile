FROM python:3.10.5-slim-buster as base

# This flag is important to output python logs correctly in docker!
ENV PYTHONUNBUFFERED 1
# Flag to optimize container size a bit by removing runtime python cache
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /code


FROM base as dep-poetry
ENV POETRY_HOME /opt/poetry
RUN python3 -m venv $POETRY_HOME
RUN $POETRY_HOME/bin/pip install poetry==1.2.2
ENV POETRY_BIN $POETRY_HOME/bin/poetry
COPY pyproject.toml poetry.lock ./
RUN $POETRY_BIN config --local virtualenvs.create false
RUN $POETRY_BIN install --no-root
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


FROM base as dep-venv
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt constraints.txt ./
RUN pip install -r requirements.txt -c constraints.txt
COPY src src