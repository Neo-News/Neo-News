# Generated by Django 3.2.5 on 2021-07-17 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0026_alter_article_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.TextField(default=1626486126.6449242),
        ),
        migrations.AlterField(
            model_name='article',
            name='preview_img',
            field=models.TextField(default='default.png'),
        ),
    ]