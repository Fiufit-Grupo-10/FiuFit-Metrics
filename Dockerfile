FROM python:3.10 as python-base

RUN mkdir app

WORKDIR /app

COPY pyproject.toml/ .

COPY . /app

RUN pip3 install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

ARG MONGO_METRICS_URL
ENV MONGO_METRICS_URL $MONGO_METRICS_URL

EXPOSE 8080

CMD ["ddtrace-run", "uvicorn", "app.main:app", "--host=0.0.0.0", "--port=80"]
