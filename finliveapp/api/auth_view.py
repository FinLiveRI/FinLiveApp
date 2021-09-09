import logging

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import EMPTY_VALUES

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from finliveapp.models import UserAccount
from finliveapp.serializers.management_serializer import UserAccountSerializer


class Login(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = auth.authenticate(username=username, password=password)

        if user:
            if not user.is_active:
                return Response({"error": "Account is locked"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                useraccount = UserAccount.objects.get(user=user)
                if useraccount.retries < 1:
                    return Response({"error": "No login retries left"}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    useraccount.retries = 5
                    useraccount.save()
                    refreshtoken = RefreshToken.for_user(user)
                    return Response({'access': str(refreshtoken.access_token), 'refresh': str(refreshtoken)},
                                    status=status.HTTP_200_OK)
        else:
            try:
                _user = User.objects.get(username=username)
                if _user not in EMPTY_VALUES:
                    useraccount = UserAccount.objects.get(user=_user)
                    if useraccount in EMPTY_VALUES:
                        _user.is_active = False
                        _user.save()
                    else:
                        useraccount.retries = useraccount.retries - 1 if useraccount.retries > 0 else 0
                        useraccount.save()
            except ObjectDoesNotExist:
                pass
            return Response({'error': "Unable to login"}, status=status.HTTP_401_UNAUTHORIZED)


class Accounts(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserAccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
