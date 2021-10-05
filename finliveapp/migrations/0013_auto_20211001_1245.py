# Generated by Django 3.2.4 on 2021-10-01 12:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('finliveapp', '0012_auto_20210916_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='organization',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='finliveapp.organization'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='equipment',
            name='equipmentid',
            field=models.IntegerField(),
        ),
        migrations.AddConstraint(
            model_name='equipment',
            constraint=models.UniqueConstraint(fields=('equipmentid', 'organization'), name='equipment_organization_unique'),
        ),
    ]
