# Generated by Django 3.2.5 on 2021-07-19 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0026_auto_20210720_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.TextField(default=1626709859.960425),
        ),
        migrations.AlterField(
            model_name='recomment',
            name='created_at',
            field=models.TextField(default=1626709859.960425),
        ),
    ]
