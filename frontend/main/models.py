from contextlib import contextmanager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import connection
from django.db import models
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.dispatch import receiver
import pika


RABBITMQ_HOST = 'rabbitmq'


@contextmanager
def get_message_channel(host):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()

    yield channel

    connection.close()


def submit_message(queue, message):
    with get_message_channel(RABBITMQ_HOST) as channel:
        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=message,
        )


class Repository(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

@receiver(post_save, sender=Repository)
def repository_post_save(sender, **kwargs):
    instance = kwargs.get('instance')
    username = instance.user.username
    reponame = instance.name
    submit_message('repo', f'create {username} {reponame}')

@receiver(post_delete, sender=Repository)
def repository_post_delete(sender, **kwargs):
    instance = kwargs.get('instance')
    username = instance.user.username
    reponame = instance.name
    submit_message('repo', f'delete {username} {reponame}')


class AuthorizedKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    authorized_key = models.TextField(default='')


def authorized_key_post_update(sender, **kwargs):
    user = kwargs.get('instance').user

    authorized_keys = [k.authorized_key for k in user.authorizedkey_set.all()]
    authorized_keys = '\n'.join(authorized_keys)

    submit_message(
        'user',
        f'set_authorized_keys {user.username} {authorized_keys}',
    )
post_save.connect(authorized_key_post_update, sender=AuthorizedKey)
post_delete.connect(authorized_key_post_update, sender=AuthorizedKey)


@receiver(post_save, sender=User)
def user_post_save(sender, **kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        submit_message('user', f'create {instance.username}')


@receiver(post_delete, sender=User)
def user_post_delete(sender, **kwargs):
    instance = kwargs.get('instance')
    submit_message('user', f'delete {instance.username}')
