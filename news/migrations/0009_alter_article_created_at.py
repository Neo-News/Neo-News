# Generated by Django 3.2.5 on 2021-07-10 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_alter_article_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.TextField(default=1625923802.819012),
        ),
    ]
