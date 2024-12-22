FROM python:3.11

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

# Code is mounted as a volume for hot reloading