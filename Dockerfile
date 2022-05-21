FROM python:3.10-alpine

RUN mkdir /app
WORKDIR /app

COPY requirements_dev.txt .
RUN pip install -r requirements_dev.txt

CMD [ "python", "-u", "./main.py" ]