# Generated by Django 4.2.2 on 2023-06-14 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_tourpackage_activities'),
    ]

    operations = [
        migrations.AddField(
            model_name='day',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]