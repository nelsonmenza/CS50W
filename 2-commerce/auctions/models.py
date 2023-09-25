from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    starting_bid = models.FloatField(validators=[MinValueValidator(0.5)])
    web_page = models.URLField(max_length=200)
    img = models.ImageField(upload_to=None, height_field=None,
                            width_field=None, max_length=None)
    active = models.BooleanField()


class Category(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'ModelName'
        verbose_name_plural = 'ModelNames'
