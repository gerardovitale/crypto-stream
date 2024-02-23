ARG PYTHON_VERSION=3.8.13
ARG IMAGE_TYPE=slim


FROM python:${PYTHON_VERSION}-${IMAGE_TYPE} as python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base as builder-base
RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential
RUN curl -sSL https://install.python-poetry.org | python3 -
WORKDIR $PYSETUP_PATH


FROM python-base as development
ARG SOURCE_PATH=cryptocom_stream
WORKDIR $PYSETUP_PATH
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
WORKDIR /app
COPY ${SOURCE_PATH} poetry.lock pyproject.toml ./
RUN poetry install --no-dev
ENTRYPOINT [ "poetry", "run", "python3", "main.py" ]
