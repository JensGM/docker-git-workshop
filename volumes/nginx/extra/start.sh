#!/bin/bash

/docker-entrypoint.sh &
/extra/mq-consumer.rb &

# Foreground the nginx process
fg %1
