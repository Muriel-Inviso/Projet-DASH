from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Your custom fields for the user model
    username = models.CharField(max_length=150, unique=True)
    lastname = models.CharField(max_length=150, null=True)
    firstname = models.CharField(max_length=150, null=True)
    uid_number = models.IntegerField(null=True)

    # Additional fields for Django's user model
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Set the custom user manager
    objects = CustomUserManager()

    # Use 'username' as the unique identifier for authentication
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
