# Generated by Django 5.1.1 on 2024-11-16 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stakes', '0005_bet_nextstate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='nextState',
            field=models.CharField(choices=[('<250', '<250'), ('250-500', '250-500'), ('500-1000', '500-1000'), ('1000-2000', '1000-2000'), ('2000-4000', '2000-4000'), ('4000-7000', '4000-7000'), ('7000-12000', '7000-12000'), ('12000-20000', '12000-20000'), ('20000-30000', '20000-30000'), ('30000-45000', '30000-45000'), ('45000-80000', '45000-80000'), ('>80000', '>80000')], max_length=15),
        ),
    ]
