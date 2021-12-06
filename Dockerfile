FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/Suport

COPY requirements.txt /usr/src/Suport/requirements.txt
RUN pip install -r /usr/src/Suport/requirements.txt

COPY . .

EXPOSE 8000
