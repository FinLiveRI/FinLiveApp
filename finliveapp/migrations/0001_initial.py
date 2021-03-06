# Generated by Django 3.2.4 on 2021-07-01 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('euid', models.CharField(max_length=256, unique=True)),
                ('name', models.CharField(max_length=128)),
                ('birthDate', models.DateField()),
                ('animalid', models.CharField(max_length=128)),
                ('arrivaldate', models.DateField()),
                ('departuredate', models.DateField(blank=True, null=True)),
                ('departurereason', models.CharField(blank=True, max_length=256, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=256)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SeedingType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField()),
                ('weight', models.DecimalField(decimal_places=3, max_digits=8)),
                ('automaticmeasurement', models.BooleanField()),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finliveapp.animal')),
            ],
        ),
        migrations.CreateModel(
            name='PregnancyCheck',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('result', models.BooleanField()),
                ('calvingdate', models.DateField()),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finliveapp.animal')),
            ],
        ),
        migrations.CreateModel(
            name='Insemination',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('bull', models.CharField(max_length=128)),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finliveapp.animal')),
                ('inseminationmethod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.seedingtype')),
            ],
        ),
        migrations.CreateModel(
            name='Calving',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('assistance', models.BooleanField()),
                ('calvingnumber', models.IntegerField()),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finliveapp.animal')),
            ],
        ),
        migrations.CreateModel(
            name='Barn',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=256)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finliveapp.organization')),
            ],
        ),
        migrations.AddField(
            model_name='animal',
            name='barn',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.barn'),
        ),
        migrations.AddField(
            model_name='animal',
            name='breed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.breed'),
        ),
        migrations.AddField(
            model_name='animal',
            name='gender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.gender'),
        ),
        migrations.AddField(
            model_name='animal',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.organization'),
        ),
    ]
