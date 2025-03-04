# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY ./lib ./lib
COPY ./routes ./routes
COPY main.py main.py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "sudo python3", "main.py"]
