# Generated by Django 3.2.5 on 2021-07-17 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0028_auto_20210717_0146'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-date', '-created_at']},
        ),
        migrations.AlterField(
            model_name='article',
            name='counted_at',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.TextField(default=1626487629.5786076),
        ),
    ]