# Generated by Django 3.2.4 on 2021-11-30 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finliveapp', '0023_gender_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='gassystem',
            name='animal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.animal'),
        ),
    ]
