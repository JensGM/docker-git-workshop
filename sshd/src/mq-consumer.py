#!/usr/bin/env python3
import logging
import os
import pika
import re
from pwd import getpwnam


logging.basicConfig(level=logging.INFO)
username_pattern = re.compile(r'^[a-zA-Z][-a-zA-Z0-9]*$')
reponame_pattern = re.compile(r'^[a-zA-Z][-_a-zA-Z0-9]*$')


def handle_user_msg(channel, method, properties, body):
    body = body.decode()
    logging.info('received message: {}'.format(body))

    try:
        op, username, *args = body.split(maxsplit=2)
        if not username_pattern.match(username):
            msg = 'Usernames must match "^[a-z][-a-z0-9]*$"'.format(username)
            raise ValueError(msg)

        if op == 'create':
            os.system('/create_user.sh {}'.format(username))
        elif op == 'delete':
            cmd = 'userdel -r {}'.format(username)
            os.system(cmd)
        elif op == 'set_authorized_keys':
            authorized_keys = args[0] if len(args) == 1 else ''
            authorized_keys_path = '/home/{}/.ssh/authorized_keys'.format(
                username)
            with open(authorized_keys_path, 'w') as f:
                f.write(authorized_keys)
            # Ensure correct permissions
            os.chmod(authorized_keys_path, 0o600)
            os.chown(authorized_keys_path, getpwnam(username).pw_uid, -1)
        else:
            raise ValueError('Invalid user message {}'.format(body))
    except Exception as e:
        logging.error('message {} failed with {}'.format(body, e))
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
    else:
        channel.basic_ack(delivery_tag=method.delivery_tag)


def handle_repo_msg(channel, method, properties, body):
    logging.info('Received repo message {}'.format(body))
    body = body.decode()

    try:
        op, username, reponame = body.split()
        if not username_pattern.match(username):
            msg = 'Usernames must match "^[a-z][-a-z0-9]*$"'.format(username)
            raise ValueError(msg)
        if not reponame_pattern.match(reponame):
            msg = 'Repository names must match "^[a-zA-Z][-_a-zA-Z0-9]*$"'.format(
                reponame)
            raise ValueError(msg)

        if op == 'create':
            cmd = '/create_repo.sh {} {}'.format(username, reponame)
            os.system(cmd)
        elif op == 'delete':
            cmd = '/delete_repo.sh {} {}'.format(username, reponame)
            os.system(cmd)
        else:
            raise ValueError('Invalid repository message {}'.format(body))
    except Exception as e:
        logging.error('message {} failed with {}'.format(body, e))
        channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
    else:
        channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        'rabbitmq-service.default.svc.cluster.local'
    ))
    channel = connection.channel()

    channel.queue_declare(queue='user')
    channel.queue_declare(queue='repo')
    channel.basic_consume(queue='user', on_message_callback=handle_user_msg)
    channel.basic_consume(queue='repo', on_message_callback=handle_repo_msg)
    logging.info('Waiting for messages')
    channel.start_consuming()


if __name__ == '__main__':
    main()
