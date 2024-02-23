from django.contrib.auth.models import AbstractUser
from django.db import models


# The class `User` is a subclass of `AbstractUser` in Python.
class User(AbstractUser):
    pass


# The `Like` class represents a user's like on a particular item, with a boolean field indicating
# whether the user has liked it or not.
class Like(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)


# This class defines a Post model with fields for username, tweet content, post date, and likes.
class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.TextField(max_length=240)
    post_date = models.DateTimeField(auto_now_add=True)
    like = models.ForeignKey(Like, on_delete=models.CASCADE)


class Follower(models.Model):
    ...
