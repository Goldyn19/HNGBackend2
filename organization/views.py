from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Organisation
from .serializers import OrganisationSerializer
from django.shortcuts import get_object_or_404
from members.models import User

class OrganisationListView(generics.ListAPIView):
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        organisations = user.organisations.all()
        serializer = self.get_serializer(organisations, many=True)
        return Response({
            "status": "success",
            "message": "Organisations retrieved successfully",
            "data": {
                "organisations": serializer.data
            }
        }, status=status.HTTP_200_OK)


class OrganisationDetailView(generics.RetrieveAPIView):
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        org_id = kwargs.get('orgId')
        organisation = get_object_or_404(Organisation, orgId=org_id)

        # Check if the requesting user is part of the organisation
        if request.user.organisations.filter(orgId=org_id).exists():
            serializer = self.get_serializer(organisation)
            return Response({
                "status": "success",
                "message": "Organisation record retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "Forbidden",
            "message": "You do not have permission to access this organisation's record",
            "statusCode": 403
        }, status=status.HTTP_403_FORBIDDEN)


class OrganisationCreateView(generics.CreateAPIView):
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            organisation = serializer.save()
            organisation.orgId = str(organisation.id)  # Ensure orgId is unique
            organisation.save()
            response_data = {
                "status": "success",
                "message": "Organisation created successfully",
                "data": {
                    "orgId": organisation.orgId,
                    "name": organisation.name,
                    "description": organisation.description
                }
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response({
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
        }, status=status.HTTP_400_BAD_REQUEST)


class AddUserToOrganisationView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        org_id = kwargs.get('orgId')
        user_id = request.data.get('userId')

        organisation = get_object_or_404(Organisation, orgId=org_id)
        user = get_object_or_404(User, userId=user_id)

        if not request.user.organisations.filter(orgId=org_id).exists():
            return Response({
                "status": "Forbidden",
                "message": "You do not have permission to modify this organisation",
                "statusCode": 403
            }, status=status.HTTP_403_FORBIDDEN)

        organisation.users.add(user)
        return Response({
            "status": "success",
            "message": "User added to organisation successfully"
        }, status=status.HTTP_200_OK)