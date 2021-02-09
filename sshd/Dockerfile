FROM python:3-buster

RUN apt-get update && apt-get install -y \
    openssh-client \
    openssh-server \
    ruby \
    ruby-dev \
    supervisor

RUN mkdir -p /run/sshd
RUN gem install pg
RUN python3 -m pip install pika psycopg2
COPY src/ /

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]
