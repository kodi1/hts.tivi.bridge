FROM python:3.11-alpine

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

RUN apk --no-cache update \
    && apk --no-cache add curl
