FROM python:3.12

ENV POETRY_VERSION = 1.7.1

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"
RUN mkdir -p /wewu-less-app
WORKDIR /wewu-less-app

# Install dependencies before copying sources to cache them
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

# Copy sources
COPY . .
