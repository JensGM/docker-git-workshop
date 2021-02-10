from contextlib import contextmanager
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import connection
from django.db import models
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
import pika


RABBITMQ_HOST = 'rabbitmq'


@contextmanager
def get_message_channel(host):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()

    yield channel

    connection.close()

class Repository(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    @staticmethod
    def post_save(sender, **kwargs):
        instance = kwargs.get('instance')
        username = instance.user.username
        reponame = instance.name
        with get_message_channel(RABBITMQ_HOST) as channel:
            channel.basic_publish(
                exchange='',
                routing_key='repo',
                body='create {} {}'.format(username, reponame)
            )

    @staticmethod
    def post_delete(sender, **kwargs):
        instance = kwargs.get('instance')
        username = instance.user.username
        reponame = instance.name
        with get_message_channel(RABBITMQ_HOST) as channel:
            channel.basic_publish(
                exchange='',
                routing_key='repo',
                body='delete {} {}'.format(username, reponame)
            )
post_save.connect(Repository.post_save, sender=Repository)
post_delete.connect(Repository.post_delete, sender=Repository)


class User(AbstractUser):
    authorized_keys = models.TextField()

    @staticmethod
    def post_save(sender, **kwargs):
        instance = kwargs.get('instance')
        created = kwargs.get('created')
        with get_message_channel(RABBITMQ_HOST) as channel:
            if created:
                channel.basic_publish(
                    exchange='',
                    routing_key='user',
                    body='create {}'.format(instance.username),
                )
            channel.basic_publish(
                exchange='',
                routing_key='user',
                body='set_authorized_keys {} {}'.format(
                    instance.username, instance.authorized_keys),
            )

    @staticmethod
    def post_delete(sender, **kwargs):
        instance = kwargs.get('instance')
        with get_message_channel(RABBITMQ_HOST) as channel:
            channel.basic_publish(
                exchange='',
                routing_key='user',
                body='delete {}'.format(instance.username),
            )
post_save.connect(User.post_save, sender=User)
post_delete.connect(User.post_delete, sender=User)
