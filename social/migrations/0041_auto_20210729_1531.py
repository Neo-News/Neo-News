# Generated by Django 3.2.5 on 2021-07-29 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0040_auto_20210726_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.TextField(default=1627540306.2473311),
        ),
        migrations.AlterField(
            model_name='recomment',
            name='created_at',
            field=models.TextField(default=1627540306.2473311),
        ),
    ]