# Generated by Django 3.2.5 on 2021-07-17 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0024_auto_20210717_0228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.TextField(default=1626491721.1073363),
        ),
        migrations.AlterField(
            model_name='recomment',
            name='created_at',
            field=models.TextField(default=1626491721.1073363),
        ),
    ]
