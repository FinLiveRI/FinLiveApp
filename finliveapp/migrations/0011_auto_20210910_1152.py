# Generated by Django 3.2.4 on 2021-09-10 11:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finliveapp', '0010_auto_20210908_1232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calving',
            old_name='calvingnumber',
            new_name='parity',
        ),
        migrations.RemoveField(
            model_name='feed',
            name='name',
        ),
        migrations.AlterField(
            model_name='animal',
            name='animalid',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='milking_event',
            name='somatic_cell_count',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.CreateModel(
            name='MirSpectrum',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('euid', models.CharField(max_length=256)),
                ('sampleid', models.CharField(max_length=256)),
                ('sample_date', models.DateField()),
                ('analysis_date', models.DateField()),
                ('analyzer', models.CharField(max_length=128)),
                ('exportid', models.CharField(max_length=128)),
                ('milking_time', models.IntegerField()),
                ('absorbance_value', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mir_spectrum_created_by', to=settings.AUTH_USER_MODEL)),
                ('laboratory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.laboratory')),
                ('milking_event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.milking_event')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mir_spectrum_modified_by', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.organization')),
            ],
            options={
                'db_table': 'mir_spectrum',
            },
        ),
        migrations.CreateModel(
            name='MilkAnalysis',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('euid', models.CharField(max_length=256)),
                ('protein', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fat', models.DecimalField(decimal_places=2, max_digits=5)),
                ('lactose', models.DecimalField(decimal_places=2, max_digits=5)),
                ('somatic_cell_count', models.DecimalField(decimal_places=2, max_digits=12)),
                ('time_stamp', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='milk_analysis_created_by', to=settings.AUTH_USER_MODEL)),
                ('farmid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.barn')),
                ('laboratory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.laboratory')),
                ('milking_event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.milking_event')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='milk_analysis_modified_by', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.organization')),
            ],
            options={
                'db_table': 'milk_analysis',
            },
        ),
        migrations.CreateModel(
            name='ManureSample',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('euid', models.CharField(max_length=256)),
                ('sampleid', models.CharField(max_length=256)),
                ('sample_date', models.DateField()),
                ('analysis_date', models.DateField()),
                ('analyzer', models.CharField(max_length=128)),
                ('nirs_n', models.IntegerField()),
                ('nirs_ndf', models.IntegerField()),
                ('nirs_indf', models.IntegerField()),
                ('nirs_omd', models.IntegerField()),
                ('nirs_dmi', models.IntegerField()),
                ('nirs_gh', models.IntegerField()),
                ('nirs_nh', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manure_sample_created_by', to=settings.AUTH_USER_MODEL)),
                ('laboratory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.laboratory')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manure_sample_modified_by', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.organization')),
            ],
            options={
                'db_table': 'manure_sample',
            },
        ),
        migrations.CreateModel(
            name='GasMeasurement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('euid', models.CharField(max_length=256)),
                ('rfid', models.CharField(default='', max_length=256)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('measurement_duration', models.IntegerField()),
                ('co2', models.IntegerField()),
                ('ch4', models.IntegerField()),
                ('o2', models.IntegerField()),
                ('h2', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gas_system_created_by', to=settings.AUTH_USER_MODEL)),
                ('equipmentid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.equipment')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gas_system_modified_by', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.organization')),
            ],
            options={
                'db_table': 'gas_system',
            },
        ),
        migrations.CreateModel(
            name='BloodSample',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('euid', models.CharField(max_length=256)),
                ('sampleid', models.CharField(max_length=256)),
                ('animalid', models.CharField(max_length=128)),
                ('time_stamp', models.DateTimeField()),
                ('glucose', models.IntegerField()),
                ('nefa', models.IntegerField()),
                ('bhba', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blood_sample_created_by', to=settings.AUTH_USER_MODEL)),
                ('laboratory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.laboratory')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blood_sample_modified_by', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='finliveapp.organization')),
            ],
            options={
                'db_table': 'blood_sample',
            },
        ),
    ]
