# Generated by Django 5.1.1 on 2024-11-20 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stakes', '0006_alter_bet_nextstate'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='method',
            field=models.CharField(choices=[('u0', 'u0'), ('u1', 'u1')], default='u0', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='betpending',
            name='method',
            field=models.CharField(choices=[('u0', 'u0'), ('u1', 'u1')], default='u0', max_length=2),
            preserve_default=False,
        ),
    ]
