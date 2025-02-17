FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3 python3-pip libcairo2 libcairo2-dev tzdata && \
    apt-get clean

WORKDIR /app

COPY ./app/requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./app .
