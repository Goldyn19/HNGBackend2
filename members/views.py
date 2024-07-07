from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import UserSerializer
from .tokens import create_jwt_pair_for_user
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

class SignUpView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = create_jwt_pair_for_user(user)

            response_data = {
                'status': 'success',
                'message': 'Registration successful',
                'data': {
                    'accessToken': tokens['access'],
                    'user': UserSerializer(user).data
                }
            }
            return Response(data=response_data, status=status.HTTP_201_CREATED)

        return Response(data={
            'status': 'Bad request',
            'message': 'Registration unsuccessful',
            'statusCode': 400,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(generics.GenericAPIView):
#
#     permission_classes = [AllowAny]
#
#     def post(self, request: Request):
#         password = request.data.get('password')
#         email = request.data.get('email')
#
#         user = authenticate(email=email, password=password)
#
#         if user is not None:
#             tokens = create_jwt_pair_for_user(user)
#             response_data = {
#                 'status': 'success',
#                 'message': 'Login successful',
#                 'data': {
#                     'accessToken': tokens['access'],
#                     'user': UserSerializer(user).data
#                 }
#             }
#             return Response(data=response_data, status=status.HTTP_200_OK)
#         else:
#             return Response(data={
#                 'status': 'Bad request',
#                 'message': 'Authentication failed',
#                 'statusCode': 401
#             }, status=status.HTTP_401_UNAUTHORIZED)

class LoginView (APIView):
    permission_classes = [AllowAny]

    def post(self, request:Request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        # user = get_object_or_404(User, email=email)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response_data = {
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'accessToken': tokens['access'],
                    'user': UserSerializer(user).data
                }
            }
            return Response(data=response_data, status=status.HTTP_200_OK)
        else:
            return Response(data={
                'status': 'Bad request',
                'message': 'Authentication failed',
                'statusCode': 401
            }, status=status.HTTP_401_UNAUTHORIZED)



class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = get_object_or_404(User, userId=user_id)

        # Check if the requesting user is the same as the user being requested
        if request.user == user:
            serializer = self.get_serializer(user)
            return Response({
                "status": "success",
                "message": "User record retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        # Check if the requesting user is part of the user's organisations
        user_organisations = user.organisations.all()
        if request.user.organisations.filter(id__in=user_organisations).exists():
            serializer = self.get_serializer(user)
            return Response({
                "status": "success",
                "message": "User record retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "Forbidden",
            "message": "You do not have permission to access this user's record",
            "statusCode": 403
        }, status=status.HTTP_403_FORBIDDEN)