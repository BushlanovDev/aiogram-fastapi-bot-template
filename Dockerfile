FROM python:3.12-slim-bullseye AS base

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100


FROM base AS builder

COPY requirements.txt requirements.txt

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt


FROM base
ENV VIRTUAL_ENV=/opt/venv
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
COPY . /app

EXPOSE 8080

ENTRYPOINT ["python", "main.py"]
