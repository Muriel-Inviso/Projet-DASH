# from django.contrib.auth.models import AbstractBaseUser
from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150, null=True)
    firstname = models.CharField(max_length=150, null=True)
    uid_number = models.IntegerField(null=True)

    def __str__(self):
        return self.username
