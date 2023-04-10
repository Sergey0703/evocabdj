import djongo
from django.db import models
from djongo import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
#from djongo.models import ObjectIdField
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class WordsModel(models.Model):
    #code = models.AutoField(unique=True, null=True)
    #ID = models.AutoField(primary_key=True)
    _id = models.ObjectIdField()
    code = models.IntegerField(default=0)
    word = models.CharField(max_length=200)
    translate = models.CharField(max_length=200)
    train1=models.BooleanField(False, null=True)
    trainDate=models.DateTimeField(auto_now=True)
    transcript=models.CharField(max_length=200,null=True)
    sound=models.CharField(max_length=200, null=True)
    updateDate=models.DateTimeField(auto_created=True, null=True)
    owner=models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'words'
        managed = False  # remove this line

    def __str__(self) -> str:
        return self.word


'''
    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum display_id value from the database
            code = self.objects.all().aggregate(largest=models.Max('code'))['largest']

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            if code is not None:
                self.code = code + 1

        super(WordsModel, self).save(*args, **kwargs)
'''
#_id = models.ObjectIdField()
#_id: ObjectIdField(primary_key=True)
