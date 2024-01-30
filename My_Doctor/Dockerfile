# Base image
FROM python:3.11


# env variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1


# Set workdir /usr/src/app
WORKDIR /usr/src/app


# install python dependencies
RUN pip install --upgrade pip
RUN pip install poetry


# install psycopg2 dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


# Copy poetry  config files 
COPY pyproject.toml poetry.lock ./


# Install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install


# Copy files 
COPY . .


# Copy .env file
RUN cp env-template-docker .env


# Run flake8
# RUN poetry run flake8 --ignore=E501,F401 ./


# Port Exposing
EXPOSE 8000


