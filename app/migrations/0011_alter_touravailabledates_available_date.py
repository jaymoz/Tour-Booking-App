# Generated by Django 4.2.2 on 2023-06-15 00:10

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_touravailabledates_available_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='touravailabledates',
            name='available_date',
            field=models.DateField(validators=[app.models.validate_start_date]),
        ),
    ]
