# Generated by Django 3.2.5 on 2021-07-21 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0031_alter_user_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.TextField(default=1626859445.9920254),
        ),
    ]
