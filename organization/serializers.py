from .models import  Organisation
from rest_framework import serializers


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['orgId', 'name', 'description']
        read_only_fields = ["orgId"]

    def create(self, validated_data):
        organisation = Organisation.objects.create(**validated_data)
        return organisation
