# Generated by Django 3.0.4 on 2020-05-12 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Globe', '0021_discussion'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscussionTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Topic', models.CharField(max_length=50)),
            ],
        ),
    ]
