# Generated by Django 3.1 on 2020-08-20 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20200820_1811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='comments',
        ),
    ]