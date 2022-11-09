FROM python:3.10
RUN python3 -m pip install Django psycopg2 pika

RUN mkdir /code
VOLUME /code
WORKDIR /code

COPY . .
RUN python3 -m pip install -r requirements.txt
CMD ["./start.sh"]
