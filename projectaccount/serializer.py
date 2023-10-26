from rest_framework import serializers
# from store.models import TeamProfile,Service
from django.contrib.auth import authenticate

# from store.serializer import SubjectSerializer
from .models import Account, Subject
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from urllib.parse import urljoin



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
    


class LogoutSerializer(serializers.Serializer):
    pass



