# Generated by Django 4.2.2 on 2023-06-15 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_tourpackage_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='TourAvailableDates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_date', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'Tour Available Dates',
                'db_table': 'TourAvailableDates',
            },
        ),
        migrations.RemoveField(
            model_name='tourpackage',
            name='number_of_people',
        ),
        migrations.AddField(
            model_name='tourpackage',
            name='full',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tourpackage',
            name='tour_dates',
            field=models.ManyToManyField(to='app.touravailabledates'),
        ),
    ]
