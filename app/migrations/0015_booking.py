# Generated by Django 4.2.2 on 2023-06-15 07:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0014_remove_tourpackage_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50)),
                ('ordered_date', models.DateTimeField()),
                ('num_of_people', models.IntegerField()),
                ('ref_code', models.CharField(max_length=10)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('cancelled', 'Cancelled')], max_length=100)),
                ('dates', models.DateField()),
                ('street_address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=20)),
                ('country', models.CharField(max_length=20)),
                ('postal_code', models.CharField(max_length=20)),
                ('grand_total', models.DecimalField(decimal_places=2, max_digits=7)),
                ('paid', models.BooleanField(default=False)),
                ('selections', models.ManyToManyField(to='app.selection')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tourpackage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Bookings',
                'db_table': 'Booking',
            },
        ),
    ]
