# Generated by Django 4.2.2 on 2023-06-14 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_tourpackage_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourpackage',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]
