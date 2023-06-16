# Generated by Django 4.2.2 on 2023-06-14 22:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Activities',
                'db_table': 'Activity',
            },
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('activity', models.ManyToManyField(to='app.activity')),
            ],
            options={
                'verbose_name_plural': 'Day',
                'db_table': 'Day',
            },
        ),
        migrations.CreateModel(
            name='Selection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
            ],
            options={
                'verbose_name_plural': 'Selections',
                'db_table': 'Selection',
            },
        ),
        migrations.CreateModel(
            name='TourPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('discount_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('start_date', models.DateTimeField()),
                ('starting_point', models.CharField(max_length=20)),
                ('number_of_people', models.IntegerField()),
                ('city', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('age', models.IntegerField()),
                ('slug', models.SlugField()),
                ('days', models.ManyToManyField(to='app.day')),
                ('selections', models.ManyToManyField(to='app.selection')),
            ],
        ),
        migrations.CreateModel(
            name='TourPackageExclusion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'TourPackageExclusions',
                'db_table': 'TourPackageExclusion',
            },
        ),
        migrations.CreateModel(
            name='TourPackageInclusion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'TourPackageInclusions',
                'db_table': 'TourPackageInclusion',
            },
        ),
        migrations.CreateModel(
            name='TourPackageImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tourpackage')),
            ],
            options={
                'verbose_name_plural': 'TourPackageImages',
                'db_table': 'TourPackageImage',
            },
        ),
        migrations.AddField(
            model_name='tourpackage',
            name='tour_package_exclusion',
            field=models.ManyToManyField(to='app.tourpackageexclusion'),
        ),
        migrations.AddField(
            model_name='tourpackage',
            name='tour_package_inclusion',
            field=models.ManyToManyField(to='app.tourpackageinclusion'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=500)),
                ('rating', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tourpackage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reviews',
                'db_table': 'Review',
            },
        ),
    ]
