# Generated by Django 2.2.6 on 2019-10-30 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0005_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page_title', models.TextField()),
                ('content', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='page_create_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
