from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=6, decimal_places=2, validators=[
                              MinValueValidator(0.50)])

    web_page = models.URLField(max_length=200, blank=True)
    img = models.ImageField(null=True, blank=True, upload_to='media/')
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Categories(models.TextChoices):
        CLOTHING = 'Clothing'
        TOYS = 'Toys'
        GAMES = 'Games'
        ELECTRONICS = 'Electronics'
        HOME = 'Home'
        SPORTS = 'Sports'
        BEAUTY = 'Beauty'
        BOOKS = 'Books'
        GROCERY = 'Grocery'
        AUTOMOTIVE = 'Automotive'
        HEALTH = 'Health'

    categories = models.CharField(max_length=100, choices=Categories.choices)

    class Meta:
        verbose_name = 'Listing'
        verbose_name_plural = 'Listings'

    def __str__(self):
        return self.title


class Comment(models.Model):
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=350)
    created_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.username)
