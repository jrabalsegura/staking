# Generated by Django 5.1.1 on 2024-09-19 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stakes', '0002_rename_multiplier_bet_next_multiplier_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='daily_profit',
            field=models.FloatField(default=0),
        ),
    ]