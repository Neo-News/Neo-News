# Generated by Django 3.2.5 on 2021-07-21 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0029_alter_user_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.TextField(default=1626835106.7101107),
        ),
    ]