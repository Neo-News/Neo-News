# Generated by Django 3.2.5 on 2021-07-21 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0037_auto_20210721_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='press',
            name='deleted_at',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.TextField(default=1626859445.9920254),
        ),
    ]
