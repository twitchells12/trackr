# Generated by Django 3.1 on 2020-09-02 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='team_pic',
            field=models.ImageField(blank=True, default='team.png', null=True, upload_to=''),
        ),
    ]
