FROM python:3.11

WORKDIR /

COPY pyproject.toml .

RUN python -m pip install poetry
# do not create a virtual environment
RUN python -m poetry config virtualenvs.create false
RUN python -m poetry install --without model

# copy necessary files
COPY .data/ ./.data
COPY recommender/ ./recommender
COPY app.py .

# command to run on container start
CMD [ "litestar", "run", "--host", "0.0.0.0", "--port", "8001" ]