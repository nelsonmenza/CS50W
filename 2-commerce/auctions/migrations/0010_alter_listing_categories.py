# Generated by Django 4.2.5 on 2023-09-29 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_listing_bid_alter_listing_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='categories',
            field=models.CharField(choices=[('Clothing', 'Clothing'), ('Toys', 'Toys'), ('Games', 'Games'), ('Electronics', 'Electronics'), ('Home', 'Home'), ('Sports', 'Sports'), ('Beauty', 'Beauty'), ('Books', 'Books'), ('Grocery', 'Grocery'), ('Automotive', 'Automotive'), ('Health', 'Health')], max_length=100),
        ),
    ]
