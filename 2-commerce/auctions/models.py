from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
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

    CATEGORIES_CHOICES = (
        (CLOTHING, 'Apparel and Clothing'),
        (TOYS, 'Toys and Games'),
        (ELECTRONICS, 'Electronics and Gadgets'),
        (HOME, 'Home and Living'),
        (SPORTS, 'Sports and Outdoor'),
        (BEAUTY, 'Beauty and Personal Care'),
        (BOOKS, 'Books and Media'),
        (FOOD, 'Food and Grocery'),
        (AUTOMOTIVE, 'Automotive and Parts'),
        (HEALTH, 'Health and Wellness')
    )

    categories = models.CharField(max_length=100, choices=CATEGORIES_CHOICES)

    class Meta:
        db_table = 'Category'
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = ''


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categories = models.ForeignKey(
        Category, on_delete=models.CASCADE)
    bid = models.FloatField(validators=[MinValueValidator(0.5)])
    web_page = models.URLField(max_length=200)
    img = models.ImageField(upload_to=None, height_field=None,
                            width_field=None, max_length=None)
    active = models.BooleanField()
