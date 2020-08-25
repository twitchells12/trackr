# Generated by Django 3.1 on 2020-08-25 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_project_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Complete', 'Complete'), ('On Hold', 'On Hold'), ('Past Due', 'Past Due')], max_length=20),
        ),
    ]