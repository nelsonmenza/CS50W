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
        CLOTHING = 'Apparel and Clothing'
        TOYS = 'Toys and Games'
        ELECTRONICS = 'Electronics and Gadgets'
        HOME = 'Home and Living'
        SPORTS = 'Sports and Outdoor'
        BEAUTY = 'Beauty and Personal Care'
        BOOKS = 'Books and Media'
        FOOD = 'Food and Grocery'
        AUTOMOTIVE = 'Automotive and Parts'
        HEALTH = 'Health and Wellness'

    categories = models.CharField(max_length=100, choices=Categories.choices)

    class Meta:
        verbose_name = 'Listing'
        verbose_name_plural = 'Listings'
