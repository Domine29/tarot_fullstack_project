# Generated by Django 4.1.4 on 2023-01-07 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DreamEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.EmailField(max_length=254)),
                ('date', models.DateField(auto_now_add=True)),
                ('description', models.TextField()),
                ('associations', models.TextField()),
                ('inner_dynamics', models.TextField()),
                ('interpretation', models.TextField()),
                ('ritual', models.TextField()),
            ],
        ),
    ]