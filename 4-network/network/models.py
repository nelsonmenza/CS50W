from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)


class Follower(models.Model):
    ...
