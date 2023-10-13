# Generated by Django 4.2.5 on 2023-10-12 18:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_user_watchlist'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'verbose_name': 'Bid'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='watchlist',
        ),
        migrations.CreateModel(
            name='WatchlistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
