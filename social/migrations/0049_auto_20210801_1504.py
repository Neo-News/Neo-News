# Generated by Django 3.2.5 on 2021-08-01 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0048_auto_20210801_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.TextField(default=1627797870.4314337),
        ),
        migrations.AlterField(
            model_name='recomment',
            name='created_at',
            field=models.TextField(default=1627797870.4314337),
        ),
    ]
