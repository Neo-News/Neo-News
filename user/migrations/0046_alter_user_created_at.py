# Generated by Django 3.2.5 on 2021-08-01 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0045_alter_user_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.TextField(default=1627787033.6126342),
        ),
    ]
