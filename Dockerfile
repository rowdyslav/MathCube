# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.12.3

FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

USER appuser
COPY --chown=appuser . .
EXPOSE 5000

ENV MONGO_URI "mongodb+srv://rowdyslav:228doxy228@cluster0.736skbi.mongodb.net/MathCube?retryWrites=true&w=majority"
CMD python main.py