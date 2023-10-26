from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.core.exceptions import PermissionDenied
from rest_framework import generics

from projectaccount.serializer import LoginSerializer
from .models import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from django.contrib.auth.views import LoginView
from rest_framework import views
from django.contrib.auth import logout
from django.http import Http404
from rest_framework.parsers import (
    JSONParser,
    FormParser,
    MultiPartParser,
    FileUploadParser,
)



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        context = {}
        if serializer.is_valid():
            user = serializer.validated_data

            username = request.data.get("username")
            password = request.data.get("password")
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)

            context["response"] = "Successfully authenticated."
            context["pk"] = user.pk
            context["username"] = username.lower()
            context["token"] = token.key
            context["role"] = user.role
            # context["subject"] = subject.name
            context["semesters"] = [semester.name for semester in user.semester.all()]
            context["subject"] = user.subject.name if user.subject else None
            context["response"] = "Successfully authenticated."
            return Response(context, status=status.HTTP_200_OK)
        else:
            context["response"] = "Error"
            context["error_message"] = "The username or password is incorrect"
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)



class LogoutView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = [JSONParser, FormParser, MultiPartParser, FileUploadParser]

    def post(self, request):
        context = {}
        try:
            request.user.auth_token.delete()
            context["response"] = "LogOut Successful."
            status_code = status.HTTP_200_OK
        except:
            context["response"] = "Error"
            context["error_message"] = "Invalid Token"
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(context, status=status_code)
