from django.contrib.auth.models import BaseUserManager
from . import models as md


class UserManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):

        if not email:
            raise ValueError('Invalid email address')
        username = self.normalize_email(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff must have is_staff = True')
        return self.create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')
        return self.create_user(email, username, password, **extra_fields)
