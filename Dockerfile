# Use an official Python runtime as a parent image
FROM --platform=linux/x86_64 python:3.10-slim

ARG PIPENV_EXTRA_ARGS

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

RUN apt-get update \
    # dependencies for building Python packages && cleaning up unused files
    && apt-get install -y build-essential \
    libcurl4-openssl-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*


# Python dependencies
RUN pip install --upgrade pip pipenv setuptools

COPY Pipfile Pipfile.lock ./
RUN pipenv sync --system ${PIPENV_EXTRA_ARGS}

# Copy project stuff
COPY ./ ./
