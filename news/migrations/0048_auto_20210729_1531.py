# Generated by Django 3.2.5 on 2021-07-29 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0047_alter_article_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='kakao_img',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.TextField(default=1627540306.2473311),
        ),
    ]
