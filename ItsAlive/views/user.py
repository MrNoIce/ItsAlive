from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import serializers




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
