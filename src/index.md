# Dockerize Python

[![](index_assets/quote-talk-is-cheap.jpg)](https://github.com/darklab8/darklab_article_docker_python)

- Репозиторий с примерами кода для данной статьи: [Github](https://github.com/darklab8/darklab_article_docker_python)

## 1. Article

### 1.0 Используемые технологии

- docker и docker-compose (книга [Docker Deep Dive](https://www.oreilly.com/library/view/docker-deep-dive/9781800565135/) рекомендуется к изучению)
- [Github Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) и [Gitlab CI](https://docs.gitlab.com/ee/ci/quick_start/)
- [Task](https://taskfile.dev/) для локальных pipeline workflow
- Python frameworks: `Django`, `FastAPI`, `Flask`
- Python ORMs + migrating libraries: `Django ORM` + `SQLALchemy`/`Alembic`
- [Self hosted Github and Gitlab runners with available docker in docker](https://github.com/darklab8/darklab_infrastructure) ()

### 1.1 Вступление

Для сборки докер контейнера нам нужно учесть следующие моменты

### 1.2 Зависимости

В Python наличествует как минимум 5 способов установки зависимостей к проекту

- pip менеджер по умолчанию, установка файлов вида `requirements.txt`, `requirements.dev.text`, `constraints.txt`
- Установка `requirements.txt` через venv
- Установка зависимостей через Pipenv package manager
- Установка зависимостей через Poetry package manager
- Установка зависимостей через Conda (common for data science/machine learning projects)

4 из них продемонстрированы в [Dockerfile](https://github.com/darklab8/darklab_article_docker_python/blob/master/example_frm_flask/Dockerfile) для Flask [простого проекта](https://github.com/darklab8/darklab_article_docker_python/tree/master/example_frm_flask).

`dep-poetry`, `dep-pipenv`, `dep-pip`, `dep-venv` docker stages демонстируруют одноименные установки зависимостей
```docker
FROM python:3.10.5-slim-buster as base

ENV PYTHONUNBUFFERED 1
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
```

Альтернативные варианты установки и настроек см. по следующим адресам:

- [poetry documentation](https://python-poetry.org/docs/#installing-with-the-official-installer)
- [pipenv documentation](https://pipenv.pypa.io/en/latest/#install-pipenv-today)
- [pip documentation](https://pip.pypa.io/en/stable/getting-started/)

### 1.3 Веб серверы

Помимо этого нужно учесть то что встроенные веб сервера в Flask/Django/FastAPI запускаемые через `python3 entryfile.py` по умолчанию
подразумеваются для использования лишь в разработке. 

Python web servers разделаются на две категории:

- WSGI based веб сервера (вида Gunicorn), использование которого подразумевается для sync Python кода (не содержающего async инструкций).
- и ASGI based веб сервера (вида Uvicorn) подразумеваемые к использванию для питон кода содержащего асинхронный код. Использование Uvicorn для прода с асинхронным кодом подразумевается в паре с Gunicorn, который имеет Uvicorn workers.

При этом дополнительный момент учесть... питон веб сервера не способны возвращать static assets css/js/jpeg and etc. Лучшей рекомендаций сегодня является использовать хотябы Nginx в режиме reverse proxy к питон веб серверу и настроенный так же возвращать static assets. Не в коем случае не стоит использовать библиотеки White noise, данное решение страшно глючит и медленно работает даже для одного пользователя.

#### 1.3.1 Django (Sync)

Django обычно достаточно настраивать для синхронного кода через WSGI. (Django Channels с веб сокетами для реализации живых чатов впрочем существует и ему нужно ASGI). [Пример настроенного Django работающего через Gunicorn-WSGI с Nginx reverse proxy serving static assets](https://github.com/darklab8/darklab_article_docker_python/tree/master/example_frm_django). Для данной настройки достаточно установить gunicorn через текущий используемый package manager (pip/poetry/pipenv), и запустить [веб сервер через gunicorn которому дали путь к WSGI.](https://github.com/darklab8/darklab_article_docker_python/blob/master/example_frm_django/docker-compose.prod.yml).

В prod варианте деплоя Python мы как минимум всегда можем указывать количество workers парарелльно обратаывающие запросы `gunicorn src.core.wsgi -b 0.0.0.0:8000 --workers 2`.

P.S. Django с отключенным `settings.Debug = False` перестает показывать static assets даже в дев сервере работающим через `python3 manage.py runserver`

#### 1.3.2 FastAPI (Async)

[Пример настроенного асинхронного проекта на FastAPI](https://github.com/darklab8/darklab_article_docker_python/tree/master/example_frm_fastapi).

Запуск меняется на `gunicorn src.core.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000`

Помимо смены веб сервера с WSGI на ASGI, асинхронные фреймворки питона требует так же асинхронно дружелюбные библиотеки и драйвера для Postgresql в том числе.
Если для синхронного Django нам достаточно установить `psycopg2-binary` pip package (Обратите внимание что psycopg2-binary не требует установки C компилирующие зависимостей в отличии от `psycopg2` библиотеки). То для асинхронного фреймворка нам нужно так же установить `asyncpg` для Postgresql)

Аналогично все библиотеки в асинхронном фреймворке должны использоваться async дружелюбные. `aiohttp` вместо `requests` к примеру для выполнения сетевых запросов.

### 1.4 CORS headers

Самая частая последняя проблема при деплое CORS headers которые должны быть часто настроены.

- Для Django это решается через [django-cors-headers](https://pypi.org/project/django-cors-headers/)
- Для FastAPI через встроенную библиотеку [CORSMiddleware](https://fastapi.tiangolo.com/tutorial/cors/)

Примеры проектов Django с Nginx в режиме CORS разрешающим все можно найти [здесь](https://github.com/darklab8/darklab_article_docker_python/tree/master/example_frm_django).

И пример для FastAPI [Здесь](https://github.com/darklab8/darklab_article_docker_python/tree/master/example_frm_fastapi)

### 1.5 Помимо прочего

Каждый из питон фреймворков имеет богатую документацию деплоя с разными решения

- [Django Deployment](https://docs.djangoproject.com/en/4.1/howto/deployment/) (Так же упомянут и полезный checklist для деплоя)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Flask deployment](https://flask.palletsprojects.com/en/2.2.x/deploying/)

Для [Django](https://github.com/darklab8/darklab_article_docker_python/tree/master/example_frm_django), [FastAPI](https://github.com/darklab8/darklab_article_docker_python/tree/master/example_frm_fastapi) (и минималистичный вариант под минималистичный [Flask)](https://github.com/darklab8/darklab_article_docker_python/tree/master/example_frm_flask) в рамках данной статьи предоставлены варианты конфигурации контейнеризации с Docker-compose и настроенными выполнениями unit тестов создающими объекты в postgresql через Pytest framework.

Обратим внимание, что Django ORM миграции БД создаваемые через `python3 manage.py makemigrations` должны быть закомиттены в репозиторий, и могут применяться к БД через `python3 manage.py migrate`.

Для FastAPI и Flask частым решением используется SQLALchemy для ORM и Alembic для миграции БД. `alembic -c src/alembic.ini revision --autogenerate -m "migration_name"` для создание миграций БД, `alembic -c src/alembic.ini upgrade head` - для применения всех до последней миграций к бд

#### 1.5.1 Static assets

Фреймворку возможно еще будет нужно добавить параметр куда собирать static assets и во время сборки докер изображения их собрать туда

Django: `./manage.py collectstatic --noinput --clear` (см. STATIC_URL / STATIC_ROOT в [settings.py](https://github.com/darklab8/darklab_article_docker_python/blob/master/example_frm_django/src/core/settings.py))

#### 1.5.2 Translations

Если в фреймворке используеться translations, понадобяться дополнительный шаг во время сборки Docker изображения для этого.

- Django: `python3 manage.py compilemessages`
- Flask: [инструкции здесь](https://flask-user.readthedocs.io/en/v0.6/internationalization.html) если используеться Flask-Babel
- FastAPI: Для FastAPI очевидных решений нет, возможно используется [gettext](https://sbabashahi.medium.com/add-translation-to-fastapi-with-gettext-a769ae6dd6bb)

#### 1.5.3 CI pipeline build && test

Предоставлены примеры настройки CI agnostic pipeline workflows через [task](https://taskfile.dev/usage/) (которые можно исполнять локально!) и docker-compose:

- для [Github Actions](https://github.com/darklab8/darklab_article_docker_python/blob/master/.github/workflows/build.yml)
- для [Gitlab CI](https://github.com/darklab8/darklab_article_docker_python/blob/master/.gitlab-ci.yml) 

## 2. FAQ

### Общее для проектов на Python
#### Приложение является самостоятельным или это виртуальный хост для  веб-сервера?

В общем случае Python веб приложения самостоятельны и деплояться через Gunicorn/Uvicorn/WSGI/ASGI и прочие веб серверы питона (см. полный список в ссылках документации по деплою фреймворков в главе 1.5)

Однако Питон веб сервера не могут возвращать static assets css/js/jpeg и тд. В этом случае их возвращают через Nginx работающим заодно в режиме reverse proxy к питон серверу.

Так же Nginx и прочие reverse proxy, используются для аугментации вида... регулирования headers, добавить client side или server side caching.

В мало популярном случае питон веб сервер можно напрямую сдеплоить через Apache mod_wsgi к примеру, но это является мало популярным решением. Если так хочеться feature rich возможностей, посмотрите в сторону [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) (Очень много фич).

И хоть и некоторые питон сервера могут TSL сертификаты прикрепить, все же проще через Nginx это сделать или иные внешние решения.

#### Приложение можно запустить в одном контейнере?

Да, можно. Если в приложении нету никаких добавок вида Celery (Message Queue), и если static assets нет необходимости возвращать (Для REST API в общем случае не нужно, если только не Django приложение с используемым Django Admin интерфейсом)

и если для кеширования не нужен Redis / или Redis деплоиться где то отдельно.

Иначе для одного даже dev environment используется множество контейнеров, контейнер под postgresql, redis, основной web server, celery beat(cron like message queue task producer), celery worker (message queue worker), celery flower (message queue monitoring) + nginx (в качестве reverse proxy + serving static assets)

[см. пример возможного большого колва контейнеров](https://github.com/darklab8/darklab_article_docker_python/blob/master/example_frm_django/docker-compose.prod.yml)

#### Требуется ли приложению установка зависимостей?

- Да, читатайте статью от главы [1.2 Зависимости](#12)
- Если проект применяет вставки C кода или какого либо вида [golang вызывать в python](https://medium.com/analytics-vidhya/running-go-code-from-python-a65b3ae34a2d). Может понадобиться установка библиотек компиляции C кода как минимум. Большие детали по разным вариантам описаны в книге `Python Expert Programming 4th edition` в главе C extensions


#### Best-practices по контейнеризации

- Те же что и везде, сжимать в один шаг установку и очистку кеша
- Использовать multi staging... Который в основном не нужен так как компилируют веб приложения к бинарникам редко
- Сначала установить зависимости, потом копировать остальной код
- Нормально Python код иметь собранными в packages от root folder, чтобы PYTHONPATH хаков с обнаружением модулей и packages не потребовалось (root папка не должны иметь `__init__.py` файл, а каждая копируемая папка с python кодом должна иметь `__init__.py` на всех уровнях. И пути импорта прописаны по человечески абсолютные от root folder или относительные)
- Использовать ENVIRONMENT variables, а не .env файлы (их можно разве что для локальной дев разработки)
- Если настроят logging library вместо print, то совсем молодцы
- флажок `ENV PYTHONUNBUFFERED 1` нужен чтобы логи нормальны из контейнеры вылезали
- флажок `ENV PYTHONDONTWRITEBYTECODE 1` тоже можно поставить, все равно кеш питон кода в контейнере лишь место лишнее занимать будет
- не забывать что `assert` синтаксис используеться лишь в тестировании, а для прода может быть и выключен. Так что лучше его не иметь в рабочем коде.
- Если будете копировать `venv` папку с уже установленными зависимостями когда либо в контейнер, учтите что его абсолютный путь не должен меняться, либо он сломаеться. Но вообще его копировать это моветон, устанавливайте зависимости в контейнерах во время сборки xD
- не копируйте мусор вида `__pycache__` в контейнер, настройте `.dockerignore`
- Как минимум настроить масштабирование количества процессов-workers (Для более feature rich вариантов можно посмотреть в сторону uWSGI)

#### Нужны ли дополнительные скрипты (bash etc) для сборки/запуска приложения?

Для веб приложений обычно нет, однако c Makefile, или [task](https://taskfile.dev/usage/) или [paver](https://pythonhosted.org/Paver/) жить проще.
Или просто делая скрипты с [argparse](https://docs.python.org/3/library/argparse.html) встроенной библиотекой. Или через `click`. Все индивидуально для веб проектов.

Для приложений собираемых в бинарники файла вида `setup.py` от [https://pypi.org/project/setuptools/](https://pypi.org/project/setuptools/), либо иные могут наличествовать чисто питон скрипты/библиотеки для сборки проектов. Список достаточно частых решений можно составить для данного случая. В рамках данной статьи сборку бинарников а так же публикацию библиотек на pypi мы не рассматриваем.

#### Что обычно кэшируется в CI/CD пайплайне ?

при контейнеризации нам ничего кешировать и не нужно так то. Однако если бы этого не было, можно было бы закешировать устанавливаемые pip packages или используемый venv (под капотом он используеться для каждого из менеджеров почти (poetry/pipenv). ОДнако в зависимости от Package manager отличается путь где кешировать их зависимости)

Gitlab CI template for python
```yaml
variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

# Pip's cache doesn't store the python packages
# https://pip.pypa.io/en/stable/topics/caching/
#
# If you want to also cache the installed packages, you have to install
# them in a virtualenv and cache it as well.
cache:
  paths:
    - .cache/pip
    - venv/
```

### Frameworks

Существуют ли еще какие-либо предварительные процедуры для приложения, кроме установки зависимостей?

#### Django

Да в статье в большинстве перечислено:

- Смена dev сервера на боевой WSGI (для синхронного питона) или ASGI (для асинхронного питона)
- Установка питона нужной версии (или использовании Docker image с нужной питон основой)
- Установка pip если отсутствует (`python3 -m ensurepip`) для установки дальнейшей зависимостей
- Установка используемого package manager (pipenv, poetry)
- Установка зависимостей
- Отключение дебага
- Смена Django секрета на что нибудь другое из ENV
- Настройка env переменных через os.environ или альтернативные решения
- Настройка CORS headers
- Настройка куда static assets собирать и скомпилировать их в одну папку (если используются html возможности Django)
- Компиляции переводов если используется, установка OS зависимостей вида `gettext`
- При использовании библиотек питона с компиляцией через C, прочие дев инструменты компиляции должна быть установлены
- Мигрировать бд потом через `python3 manage.py migrate`

См. [пример докер файла для Django](https://github.com/darklab8/darklab_article_docker_python/blob/master/example_frm_django/Dockerfile)

#### FastAPI

В основном повторяет Django шаги, некоторые вещи повторно не упоминаются:

- Смена сервера на боевой асинхронный ASGI сервер (Для примера Gunicorn с Uvicorn workers), с увеличением колва workers
- Настройка CORS headers
- Установка используемого package manager (pipenv, poetry)
- Установка зависимостей
- Мигрировать бд потом для SQLALchemy через: `alembic -c src/alembic.ini upgrade head` (или иной используемый ORM)

См. [пример докер файла для FastAPI](https://github.com/darklab8/darklab_article_docker_python/blob/master/example_frm_fastapi/Dockerfile)

#### Flask

В основном повторяет Django шаги, некоторые вещи повторно не упоминаются:

- Смена dev сервера на боевой WSGI (для синхронного питона) или ASGI (для асинхронного питона)
- Отключение дебага
- Установка используемого package manager (pipenv, poetry)
- Установка зависимостей
- Настройка CORS headers
- Настройка куда static assets собирать и скомпилировать их в одну папку (если используются html возможности Django)
- Компиляции переводов если используется (Flask-Babel?), установка OS зависимостей вида `gettext`
- Мигрировать бд потом для SQLALchemy через: `alembic -c src/alembic.ini upgrade head` (или иной используемый ORM)
