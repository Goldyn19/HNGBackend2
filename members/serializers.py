from rest_framework import serializers
from rest_framework.validators import ValidationError
from .models import User
from organization.models import Organisation
from organization.generate import generate_org_id
import re


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=80)
    userId = serializers.CharField(max_length=255, read_only=True)
    firstName = serializers.CharField(max_length=255)
    lastName = serializers.CharField(max_length=255)
    password = serializers.CharField( write_only=True)
    phone = serializers.CharField(max_length=15, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['userId', 'firstName', 'lastName', 'email', 'password', 'phone']
        read_only_fields = ["userId"]

    def validate(self, attrs):

        if not attrs['firstName']:
            raise ValidationError({'firstName': 'First Name must not be null'})

        if not attrs['lastName']:
            raise ValidationError({'lastName': 'Last Name must not be null'})

        if not attrs['email']:
            raise ValidationError({'email': 'Email must not be null'})

        if User.objects.filter(email=attrs['email']).exists():
            raise ValidationError({'email': 'Email already exists'})

        if not re.match(r"[^@]+@[^@]+\.[^@]+", attrs['email']):
            raise ValidationError({'email': 'Invalid email format'})

        if not attrs['password']:
            raise ValidationError({'password': 'Password must not be null'})


        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        org_name = f"{validated_data['firstName']}'s Organisation"
        org_id = generate_org_id()
        organization = Organisation.objects.create(orgId=org_id, name=org_name)

        # Add user to the organization
        organization.users.add(user)
        return user


