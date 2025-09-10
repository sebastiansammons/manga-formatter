FROM python:3.9-slim-bookworm

WORKDIR /manga-formatter
COPY /src .
COPY requirements.txt .

RUN apt-get update && apt-get install -y python3-pip && pip3 install -r requirements.txt 

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

ENV PUID="1000"
ENV PGID="1000"

VOLUME /manga /appdata

EXPOSE 5000

CMD ["flask", "run"]