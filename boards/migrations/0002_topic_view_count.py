# Generated by Django 2.0.2 on 2018-02-12 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='view_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
