# Generated by Django 4.2.2 on 2023-06-15 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_touravailabledates_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='touravailabledates',
            name='available_date',
            field=models.DateField(),
        ),
    ]
