# Generated by Django 3.2.4 on 2021-12-16 11:18

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('finliveapp', '0029_auto_20211216_1018'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='animal',
            managers=[
                ('api', django.db.models.manager.Manager()),
            ],
        ),
    ]