# Generated by Django 4.2.2 on 2023-06-11 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_alter_user_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Auction',
            new_name='Items',
        ),
    ]