# Generated by Django 4.2.2 on 2023-06-15 00:02

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_tourpackage_discount_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourpackage',
            name='start_date',
            field=models.DateTimeField(validators=[app.models.validate_start_date]),
        ),
    ]
