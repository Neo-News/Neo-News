# Generated by Django 3.2.5 on 2021-07-11 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_auto_20210711_0307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.TextField(default=1625995710.6939337),
        ),
        migrations.AlterField(
            model_name='recomment',
            name='created_at',
            field=models.TextField(default=1625995710.6939337),
        ),
    ]
