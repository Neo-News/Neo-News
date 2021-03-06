# Generated by Django 3.2.5 on 2021-07-09 16:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('news', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='articleshare',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='article_share', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article', to='user.category'),
        ),
        migrations.AddField(
            model_name='article',
            name='keyword',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article', to='user.keyword'),
        ),
        migrations.AddField(
            model_name='article',
            name='potal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='potal', to='news.potal'),
        ),
        migrations.AddField(
            model_name='article',
            name='press',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='press', to='news.press'),
        ),
    ]
