# Generated by Django 4.1.1 on 2022-10-16 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_bid_alter_listing_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.FloatField(),
        ),
    ]
