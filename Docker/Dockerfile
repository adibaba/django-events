FROM python:3.11.4-slim-bookworm

WORKDIR /srv

# Force the stdout and stderr streams to be unbuffered
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements_prod.txt .
RUN pip install -r requirements_prod.txt

COPY . .

EXPOSE 8000