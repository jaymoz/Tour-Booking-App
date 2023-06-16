# Generated by Django 4.2.2 on 2023-06-15 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_remove_booking_dates_alter_booking_ordered_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('message', models.TextField()),
                ('email', models.CharField(max_length=100)),
                ('read', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'Contact',
            },
        ),
    ]
