# Generated by Django 4.1.7 on 2023-06-05 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='type',
        ),
    ]