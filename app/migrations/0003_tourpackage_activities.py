# Generated by Django 4.2.2 on 2023-06-14 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_tourpackageexclusion_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourpackage',
            name='activities',
            field=models.ManyToManyField(to='app.activity'),
        ),
    ]
