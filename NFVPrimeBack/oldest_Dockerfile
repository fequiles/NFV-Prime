# syntax=docker/dockerfile:1

FROM python:3.8.10 as base
WORKDIR /python-docker

COPY ./lib ./lib
COPY ./routes ./routes
COPY ./Arquivos ./Arquivos
COPY main.py main.py
COPY config_NFV_Prime.sh config_NFV_Prime.sh
COPY config_NFV_Client.sh config_NFV_Client.sh
# RUN pip3 install -r requirements.txt
RUN pip3 install Flask Flask-Cors psycopg2
RUN apt -y update
RUN apt-get install -y net-tools

COPY . .

CMD ["python3", "main.py"]
