from random import randint

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import ConfirmationCode
from . import serializers


@api_view(['POST'])
def register_api_view(request):

    serializer = serializers.RegisterSerializer(
        data=request.data
    )

    serializer.is_valid(raise_exception=True)

    user = User.objects.create_user(
        username=serializer.validated_data['username'],
        email=serializer.validated_data['email'],
        password=serializer.validated_data['password'],
        is_active=False
    )

    code = str(randint(100000, 999999))

    ConfirmationCode.objects.create(
        user=user,
        code=code
    )

    return Response(
        {
            'message': 'user created',
            'code': code
        },
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
def confirm_api_view(request):

    serializer = serializers.ConfirmSerializer(
        data=request.data
    )

    serializer.is_valid(raise_exception=True)

    try:
        confirmation = ConfirmationCode.objects.get(
            code=serializer.validated_data['code']
        )
    except ConfirmationCode.DoesNotExist:
        return Response(
            {'error': 'invalid code'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = confirmation.user
    user.is_active = True
    user.save()

    confirmation.delete()

    return Response(
        {'message': 'user confirmed'}
    )

@api_view(['POST'])
def login_api_view(request):

    serializer = serializers.LoginSerializer(
        data=request.data
    )

    serializer.is_valid(raise_exception=True)

    user = authenticate(
        username=serializer.validated_data['username'],
        password=serializer.validated_data['password']
    )

    if not user:
        return Response(
            {'error': 'invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    return Response(
        {'message': 'login success'}
    )