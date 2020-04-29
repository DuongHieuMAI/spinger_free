FROM python:3.8-buster

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install bash -y
RUN apt-get install wait-for-it -y

COPY ./src/crawler/requirements .
RUN pip install -r requirements

# Copy entrypoint
COPY ./docker/crawler/docker-entrypoint.sh /usr/local/bin/crawler-entrypoint.sh
RUN chmod +x  /usr/local/bin/crawler-entrypoint.sh
RUN ln -s /usr/local/bin/crawler-entrypoint.sh /

WORKDIR /var/app
