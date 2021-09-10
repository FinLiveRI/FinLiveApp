import uuid
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint

from finliveapp.constants import UserType


class UserAccount(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    retries = models.IntegerField(default=5)
    usertype = models.CharField(max_length=9, choices=UserType.choices(), default=UserType.VIEWER)
    created = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, related_name='user_account_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(User, related_name='user_account_modified_by', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username


class Breed(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(unique=True)
    abbreviation = models.CharField(max_length=8)
    name = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='breed_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='breed_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'breed'


class Gender(models.Model):
    id = models.AutoField(primary_key=True)
    abbreviation = models.CharField(max_length=8)
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'gender'


class Laboratory(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='laboratory_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='laboratory_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'laboratory'


class SeedingType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='seedingtype_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='seedingtype_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'seedingtype'


class Equipment(models.Model):
    id = models.AutoField(primary_key=True)
    equipmentid = models.IntegerField()
    type = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='equipment_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='equipment_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'equipment'


class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True, blank=False)
    description = models.CharField(max_length=256, null=True, blank=True)
    apikey = models.CharField(max_length=64, default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='organization_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='organization_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'organization'


class AccountOrganization(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    default = models.BooleanField(default=False)

    class Meta:
        db_table = 'account_organization'

        
class Barn(models.Model):
    id = models.AutoField(primary_key=True)
    farmid = models.IntegerField(unique=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='barn_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='barn_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'barn'


class MilkingSystem(models.Model):
    id = models.AutoField(primary_key=True)
    equipment_id = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True)
    barn = models.ForeignKey(Barn, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='milking_system_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='milking_system_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'milking_system'


class Animal(models.Model):
    id = models.AutoField(primary_key=True)
    euid = models.CharField(max_length=256)
    name = models.CharField(max_length=128)
    breed = models.ForeignKey(Breed, on_delete=models.SET_NULL, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    birthdate = models.DateField()
    animalid = models.CharField(max_length=128)
    rfid = models.CharField(max_length=256, default="")
    barn = models.ForeignKey(Barn, on_delete=models.SET_NULL, null=True)
    arrivaldate = models.DateField()
    departuredate = models.DateField(null=True, blank=True)
    departurereason = models.CharField(max_length=256, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='animal_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='animal_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'animal'
        constraints = [UniqueConstraint(fields=['euid', 'organization'], name='euid_organization_unique')]


class Weight(models.Model):
    id = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField()
    weight = models.DecimalField(max_digits=8, decimal_places=3)
    automaticmeasurement = models.BooleanField()
    equipment_id = models.CharField(max_length=128, default="")
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='weight_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='weight_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'weight'


class Calving(models.Model):
    id = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    assistance = models.CharField(max_length=128, blank=True)
    parity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='calving_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='calving_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'calving'


class Insemination(models.Model):
    id = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    bull = models.CharField(max_length=128)
    insemination_method = models.ForeignKey(SeedingType, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='insemination_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='insemination_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'insemination'


class PregnancyCheck(models.Model):
    id = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    result = models.BooleanField()
    calvingdate = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='pregnancycheck_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='pregnancycheck_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'pregnancycheck'


class Feed(models.Model):
    id = models.AutoField(primary_key=True)
    feed_id = models.CharField(max_length=256)
    mixing_date = models.DateField()
    fresh_weight = models.DecimalField(max_digits=10, decimal_places=3)
    dry_matter_content = models.IntegerField()
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='feed_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='feed_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'feed'


class FeedAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    sample_id = models.CharField(max_length=256)
    location = models.CharField(max_length=128, null=True, blank=True)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.SET_NULL, null=True)
    analysis_number = models.CharField(max_length=64)
    feed = models.ForeignKey(Feed, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    experiment_number = models.CharField(max_length=128)
    sample_start_date = models.DateField()
    sample_end_date = models.DateField(null=True)
    primary_dry_matter = models.IntegerField(null=True)
    secondary_dry_substance = models.IntegerField(null=True)
    ash_content = models.IntegerField(null=True)
    crude_protein = models.IntegerField(null=True)
    fat = models.IntegerField(null=True)
    ndf = models.IntegerField(null=True)
    indf = models.IntegerField(null=True)
    adf = models.IntegerField(null=True)
    starch = models.IntegerField(null=True)
    aia = models.IntegerField(null=True)
    cellulase_solubility = models.IntegerField(null=True)
    digestivity = models.IntegerField(null=True)
    d_value = models.IntegerField(null=True)
    ph = models.DecimalField(max_digits=4, decimal_places=2)
    sugar = models.DecimalField(max_digits=5, decimal_places=2)
    nh3_n = models.DecimalField(max_digits=5, decimal_places=2)
    ethanol = models.DecimalField(max_digits=5, decimal_places=2)
    total_n = models.DecimalField(max_digits=5, decimal_places=2)
    lactic_acid = models.DecimalField(max_digits=5, decimal_places=2)
    acetic_acid = models.DecimalField(max_digits=5, decimal_places=2)
    propionic_acid = models.DecimalField(max_digits=5, decimal_places=2)
    butyric_acid = models.DecimalField(max_digits=5, decimal_places=2)
    isobutyric_acid = models.DecimalField(max_digits=5, decimal_places=2)
    isovaleric_acid = models.DecimalField(max_digits=5, decimal_places=2)
    capronic_acid = models.DecimalField(max_digits=5, decimal_places=2)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='feed_analysis_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='feed_analysis_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'feed_analysis'


class Feeding(models.Model):
    id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    visit_start_time = models.DateTimeField()
    visit_end_time = models.DateTimeField(null=True)
    visit_duration = models.IntegerField(blank=True, null=True)
    feed_weight = models.DecimalField(max_digits=6, decimal_places=3)
    feed_consumption = models.DecimalField(max_digits=6, decimal_places=3)
    feed = models.ForeignKey(Feed, on_delete=models.SET_NULL, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='feeding_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='feeding_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'feeding'


class Milking_Event(models.Model):
    id = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    barn = models.ForeignKey(Barn, on_delete=models.CASCADE)
    total_milk_weight = models.DecimalField(max_digits=6, decimal_places=3)
    rf_milk = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    rb_milk = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    lf_milk = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    lb_milk = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    rf_conductivity = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    rb_conductivity = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    lf_conductivity = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    lb_conductivity = models.DecimalField(max_digits=6, decimal_places=3, null=True)
    somatic_cell_count = models.DecimalField(max_digits=12, decimal_places=2)
    colour = models.CharField(max_length=64, null=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    total_flow_duration = models.IntegerField(null=True)
    rf_flow_duration = models.IntegerField(null=True)
    rb_flow_duration = models.IntegerField(null=True)
    lf_flow_duration = models.IntegerField(null=True)
    lb_flow_duration = models.IntegerField(null=True)
    milking_system = models.ForeignKey(MilkingSystem, on_delete=models.SET_NULL, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='milking_event_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='milking_event_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'milking_event'


class GasSystem(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    equipmentid = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True)
    euid = models.CharField(max_length=256)
    rfid = models.CharField(max_length=256, default="")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    measurement_duration = models.IntegerField()
    co2 = models.IntegerField()
    ch4 = models.IntegerField()
    o2 = models.IntegerField()
    h2 = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='gas_system_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='gas_system_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'gas_system'


class MilkAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.SET_NULL, null=True)
    milking_event = models.ForeignKey(Milking_Event, on_delete=models.SET_NULL, null=True)
    farmid = models.ForeignKey(Barn, on_delete=models.SET_NULL, null=True)
    euid = models.CharField(max_length=256)
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    fat = models.DecimalField(max_digits=5, decimal_places=2)
    lactose = models.DecimalField(max_digits=5, decimal_places=2)
    somatic_cell_count = models.DecimalField(max_digits=12, decimal_places=2)
    time_stamp = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='milk_analysis_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='milk_analysis_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'milk_analysis'


class BloodSample(models.Model):
    id = models.AutoField(primary_key=True)
    euid = models.CharField(max_length=256)
    sampleid = models.CharField(max_length=256)
    animalid = models.CharField(max_length=128)
    time_stamp = models.DateTimeField()
    glucose = models.IntegerField()
    nefa = models.IntegerField()
    bhba = models.IntegerField()
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='blood_sample_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='blood_sample_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'blood_sample'


class ManureSample(models.Model):
    id = models.AutoField(primary_key=True)
    euid = models.CharField(max_length=256)
    sampleid = models.CharField(max_length=256)
    sample_date = models.DateField()
    analysis_date = models.DateField()
    analyzer = models.CharField(max_length=128)
    nirs_n = models.IntegerField()
    nirs_ndf = models.IntegerField()
    nirs_indf = models.IntegerField()
    nirs_omd = models.IntegerField()
    nirs_dmi = models.IntegerField()
    nirs_gh = models.IntegerField()
    nirs_nh = models.IntegerField()
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='manure_sample_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='manure_sample_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'manure_sample'


class MirSpectrum(models.Model):
    id = models.AutoField(primary_key=True)
    euid = models.CharField(max_length=256)
    sampleid = models.CharField(max_length=256)
    sample_date = models.DateField()
    analysis_date = models.DateField()
    analyzer = models.CharField(max_length=128)
    exportid = models.CharField(max_length=128)
    milking_time = models.IntegerField()
    absorbance_value = models.IntegerField()
    milking_event = models.ForeignKey(Milking_Event, on_delete=models.SET_NULL, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='mir_spectrum_created_by', on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, related_name='mir_spectrum_modified_by', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'mir_spectrum'
