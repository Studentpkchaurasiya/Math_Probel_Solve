# Generated by Django 5.2.4 on 2025-07-11 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solver', '0002_problem_userproblemstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='standard',
            field=models.IntegerField(default=None),
        ),
    ]
