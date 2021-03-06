# Generated by Django 4.0.3 on 2022-03-26 12:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=25, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.BooleanField(default=False)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=25)),
                ('title', models.CharField(max_length=254, unique=True)),
                ('content', models.TextField()),
                ('link', models.URLField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
