# Generated by Django 3.2.5 on 2021-07-11 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_user_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('url', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.TextField(default=1625991630.3663633),
        ),
    ]