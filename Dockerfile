
# CUNY_course Docker image
# inspired by https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0

# set start-image (alternative could be the older. robust python:3.11-buster)
FROM python:3.11-bookworm

# add git for poetry package installments
RUN apt-get update && apt-get install -y git

# install specified poetry, avoiding breaking changes from one minor version to another
RUN pip install poetry==1.8.2

# set up poetry env values, including creating a isolated virtual env inside a the container
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# set root dir
WORKDIR /app

# copy all relevant files for poetry and dependency installations (exclusively!)
COPY pyproject.toml poetry.lock ./
# if needed:
# COPY dist ./dist
# COPY models ./models

# Set as environment variable for use in runtime
ARG ACCESS_TOKEN
ENV ACCESS_TOKEN=${ACCESS_TOKEN}

# configure organizational github dependencies to use CicleCI access token
RUN git config --global url."https://$ACCESS_TOKEN@github.com/drdk/".insteadOf "https://github.com/drdk/"

# poetry will complain if a README.md is not found
RUN touch README.md

# build the virtual environment and only later COPY the codebase (no root)
RUN poetry install --without dev,test,docs --no-root && rm -rf $POETRY_CACHE_DIR

# subsequently copy application code, to avoid entire image rebuilds with code chance
COPY CUNY_course ./CUNY_course
COPY tools ./tools
# if needed:
# COPY plugins ./plugins
# COPY config.yaml ./

# install the project code base in the virtual environment
RUN poetry install --without dev,test,docs

# specify entrypoint. This is the project __main__.py file
ENTRYPOINT ["poetry", "run", "CUNY_course"]