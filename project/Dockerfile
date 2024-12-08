FROM python:3.9-alpine as project

WORKDIR /usr/src/project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./reqirements.txt ./

RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install --no-cache-dir -r ./reqirements.txt

COPY . .