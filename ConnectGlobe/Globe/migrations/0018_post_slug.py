# Generated by Django 3.0.4 on 2020-05-08 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Globe', '0017_postcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.CharField(default='', max_length=130),
            preserve_default=False,
        ),
    ]