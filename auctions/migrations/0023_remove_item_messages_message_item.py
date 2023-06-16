# Generated by Django 4.2.2 on 2023-06-15 03:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_remove_bid_amount_remove_bid_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='messages',
        ),
        migrations.AddField(
            model_name='message',
            name='item',
            field=models.ForeignKey(blank=True, default=False, on_delete=django.db.models.deletion.CASCADE, to='auctions.item'),
        ),
    ]
