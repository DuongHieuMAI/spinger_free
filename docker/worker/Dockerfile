FROM python:3.8-buster

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install bash -y
RUN apt-get install wait-for-it -y

COPY ./src/worker/requirements/* ./
RUN pip install -r dev.txt

# Copy entrypoint
COPY ./docker/worker/docker-entrypoint.sh /usr/local/bin/worker-entrypoint.sh
RUN chmod +x  /usr/local/bin/worker-entrypoint.sh
RUN ln -s /usr/local/bin/worker-entrypoint.sh /

WORKDIR /app
