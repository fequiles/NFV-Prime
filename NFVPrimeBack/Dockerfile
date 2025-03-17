# syntax=docker/dockerfile:1

FROM ubuntu:20.04

WORKDIR /python-docker

COPY ./lib ./lib
COPY ./routes ./routes
COPY main.py main.py
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt-get install -y python3.8 python3-pip
# RUN pip3 install -r requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install Flask Flask-Cors psycopg2-binary 

COPY . .

VOLUME /var/lib/postgresql/data
CMD ["python3", "main.py"]

