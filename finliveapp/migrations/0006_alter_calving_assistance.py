# Generated by Django 3.2.4 on 2021-07-29 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finliveapp', '0005_rename_birthdate_animal_birthdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calving',
            name='assistance',
            field=models.CharField(default='', max_length=128),
        ),
    ]
