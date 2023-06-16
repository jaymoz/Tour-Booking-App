# Generated by Django 4.2.2 on 2023-06-14 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_day_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourpackage',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tourpackage',
            name='start_date',
            field=models.DateField(),
        ),
    ]