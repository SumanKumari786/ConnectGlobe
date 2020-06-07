# Generated by Django 3.0.4 on 2020-04-30 18:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Globe', '0013_auto_20200430_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='liked',
            field=models.ManyToManyField(blank=True, default='Like', related_name='liked', to=settings.AUTH_USER_MODEL),
        ),
    ]