from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from organization.models import Organisation



class CustomUserManger(BaseUserManager):
    def create_user(self, userId, firstName, lastName, email,  password=None, **extra_fields):
        if not userId:
            raise ValueError("The User ID must be set")
        if not firstName:
            raise ValueError("The First Name must be set")
        if not lastName:
            raise ValueError("The Last Name must be set")
        if not email:
            raise ValueError("The Email must be set")
        if not password:
            raise ValueError("The Password must be set")
        email = self.normalize_email(email)
        user = self.model(userId=userId, firstName=firstName, lastName=lastName, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userId, firstName, lastName, email,  password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('The User has to be a staff')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser must be true')
        return self.create_user(userId=userId, firstName=firstName, lastName=lastName, email=email, password=password, **extra_fields)


class User(AbstractBaseUser):
    userId = models.CharField(max_length=255, unique=True)
    firstName = models.CharField(max_length=255, null=False)
    lastName = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False, validators=[EmailValidator])
    password = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=15, blank=True, null=True)
    organisations = models.ManyToManyField(Organisation, related_name='users')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManger()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'userId']

    def __str__(self):
        return self.userId

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

# Create your models here.
