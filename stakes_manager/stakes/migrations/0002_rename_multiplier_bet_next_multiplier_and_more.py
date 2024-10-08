# Generated by Django 5.1.1 on 2024-09-17 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stakes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bet',
            old_name='multiplier',
            new_name='next_multiplier',
        ),
        migrations.RemoveField(
            model_name='betpending',
            name='multiplier',
        ),
        migrations.AddField(
            model_name='bet',
            name='next_stake',
            field=models.FloatField(default=2),
            preserve_default=False,
        ),
    ]
