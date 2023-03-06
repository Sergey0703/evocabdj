from django.contrib.auth.models import User
from evocabapi.models import WordsModel
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class WordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordsModel
        fields = ['Word', 'Translate']
