# Generated by Django 2.2.6 on 2019-10-30 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='premium_type',
            field=models.IntegerField(default=0, verbose_name='premium_type'),
        ),
    ]