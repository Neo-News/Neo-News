# Generated by Django 3.2.5 on 2021-07-10 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0004_auto_20210710_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.TextField(default=1625933798.4641204),
        ),
        migrations.AlterField(
            model_name='recomment',
            name='created_at',
            field=models.TextField(default=1625933798.4641204),
        ),
    ]