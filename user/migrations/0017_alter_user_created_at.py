# Generated by Django 3.2.5 on 2021-07-13 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_alter_user_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.TextField(default=1626182719.0320191),
        ),
    ]