FROM python:3.8

RUN mkdir /app/
COPY . /app/
WORKDIR /app

EXPOSE 8080

ENV PYTHONPATH="/app/"

RUN python3.8 -m pip install -r /app/requirements.txt

ENTRYPOINT python3.8 /app/app.py
