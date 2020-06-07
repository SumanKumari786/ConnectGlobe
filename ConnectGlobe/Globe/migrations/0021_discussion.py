# Generated by Django 3.0.4 on 2020-05-12 13:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Globe', '0020_auto_20200509_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'entries',
            },
        ),
    ]