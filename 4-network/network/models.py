from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Like(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)


class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.TextField(max_length=240)
    post_date = models.DateTimeField(auto_now_add=True)
    like = models.ForeignKey(Like, on_delete=models.CASCADE)


class Follower(models.Model):
    ...
