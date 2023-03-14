from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django_rest.http import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import WordsModel
from .serializers import WordsSerializer
from bson.objectid import ObjectId
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser


class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class ViewWords(APIView):
    model=WordsModel

    def get_object(self, pk):
        try:
            return WordsModel.objects.get(_id=ObjectId(str(pk)))
        except WordsModel.DoesNotExist:
            return Http404


    def get(self, request, *args, **kwargs):
        #queryset = WordsModel.objects.all().values()
        queryset = WordsModel.objects.order_by('updateDate').values()[:1] #filter(train1=True).values()
        print("GET")
        #return JsonResponse({'title': list(queryset)})
        return Response({'title': queryset})
        #queryset = WordsModel.objects.all()
        #words_serializer = WordsSerializer

    def post(self, request, format=None):
        #text=request.data.get("text")
        serializer = WordsSerializer(data=request.data)
        #obj = self.get_object(request.data.get("code"))
        #print(obj)
        #serializer = WordsSerializer(obj, data=request.data, partial=True)
        #print(serializer)
        #if serializer.is_valid(raise_exception=True):
        if serializer.is_valid():
            #serializer.update(obj, request.data)
            #obj.train1=True
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        obj = self.get_object(request.data.get("_id"))
        print("obj=")
        print(obj.word)

        serializer = WordsSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            #serializer.save()
            serializer.update(obj, request.data)
            print("Save!!!!!!!!!!!"+request.data.get("code"))
            #serializer.update(obj, request.data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        #train1=request.data.get("train1")
        #print(train1);
        #return Response("test", status.HTTP_201_CREATED)
        #serializer = WordsSerializer(data=request.data)
        #employee = get_object_or_404(Employee, id=employee_id)
        #if serializer.is_valid(raise_exception=True):
        #    serializer.update(serializer, request.data)
        #    return Response(serializer.data)
        #return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)