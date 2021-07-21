# Generated by Django 3.2.5 on 2021-07-21 09:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0038_auto_20210721_1824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='press',
            name='users',
        ),
        migrations.AlterField(
            model_name='article',
            name='created_at',
            field=models.TextField(default=1626860949.2772212),
        ),
        migrations.CreateModel(
            name='UserPress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.BooleanField(default=False)),
                ('press', models.ManyToManyField(blank=True, related_name='user_press', to='news.Press')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
