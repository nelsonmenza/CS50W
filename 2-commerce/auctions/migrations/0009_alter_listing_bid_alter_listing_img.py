# Generated by Django 4.2.5 on 2023-09-29 17:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_listing_options_alter_listing_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='bid',
            field=models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.5)]),
        ),
        migrations.AlterField(
            model_name='listing',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
