FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1

ADD . /app
WORKDIR /app

RUN apt-get update \
    && apt-get clean

RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/