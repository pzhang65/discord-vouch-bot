# Pulling base image
FROM python:3.8.7-alpine

RUN apk --no-cache add gcc musl-dev

# Set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# add and install requirements
COPY . .

RUN pip install pipenv

RUN pipenv install --system --deploy --ignore-pipfile

CMD ["python", "bot.py"]
