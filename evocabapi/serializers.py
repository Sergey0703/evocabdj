from bson.errors import InvalidId
from django.contrib.auth.models import User
from .models import WordsModel
from rest_framework import serializers
from bson.objectid import ObjectId
#from bson.errors import InvalidID


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ObjectIdField(serializers.Field):
    """ Serializer field for Djongo ObjectID fields """
    def to_internal_value(self, data):
        print("!!!!!")
      # Serialized value -> Database value
        try:
            return ObjectId(str(data))  # Get the ID, then build an ObjectID instance using it
        except InvalidId:
            raise serializers.ValidationError(
            '`{}` is not a valid ObjectID'.format(data))

    def to_representation(self, value):
      # Database value -> Serialized value
      if not ObjectId.is_valid(value):  # User submitted ID's might not be properly structured
        raise InvalidId
        return smart_text(value)


class WordsSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)

    class Meta:
        model = WordsModel
        fields = ['_id', 'code', 'train1', 'word']
        #fields = '__all__'

    def update(self, instance, validated_data):
        #instance.train1 = validated_data.get('train1', instance.train1)
        #instance.train1 = validated_data.get('train1')
        instance.train1 = validated_data.get('train1')
        #instance.code = validated_data.get('code')

        print("Update!!!")
        #validated_data.pop("train1", True)
        #instance.save()
        #return super().update(instance, validated_data)
        instance.save()
        return instance