# Generated by Django 4.1.4 on 2023-01-03 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarot_app', '0009_spread_date_created_spread_date_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteuser',
            name='phoneCode',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]