from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class WordsModel(models.Model):
    word = models.CharField(max_length=200)
    translate = models.CharField(max_length=200)
    train1=models.BooleanField(False)
    trainDate=models.DateTimeField(auto_now=True)
    transcript=models.CharField(max_length=200)
    sound=models.CharField(max_length=200)
    updateDate=models.DateTimeField(auto_created=True)
    owner=models.CharField(auto_created=True)


