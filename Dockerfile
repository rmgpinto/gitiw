FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY src/api.py api.py

ENV WORKERS 4

CMD ["bash", "-c", "gunicorn -w ${WORKERS} -b 0.0.0.0 api:app"]
