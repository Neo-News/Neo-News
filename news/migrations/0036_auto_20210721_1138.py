# Generated by Django 3.2.5 on 2021-07-21 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0035_alter_article_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-created_at', '-date']},
        ),
        migrations.AddField(
            model_name='press',
            name='deleted_at',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.TextField(default=1626835106.7101107),
        ),
    ]
