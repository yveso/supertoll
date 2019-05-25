FROM python:3.7.2-slim

RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get clean

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD flask run --host=0.0.0.0
