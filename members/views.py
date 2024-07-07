from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from .serializers import UserSerializer
from .tokens import create_jwt_pair_for_user
from django.contrib.auth import authenticate


class SignUpView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'User created successfully',
                'data': serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data={
            'errors': [
                {
                    'field': key,
                    'message': value[0] if isinstance(value, list) else value
                } for key, value in serializer.errors.items()
            ]
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginView(APIView):

    def post(self, request: Request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response = {
                'message': 'login successful',
                'tokens':tokens
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': 'User does not exist'})
