from django.contrib.auth.models import User
from django.db import models


class Breed(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(unique=True)
    abbreviation = models.CharField(max_length=8)
    name = models.CharField(max_length=128)

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

    class Meta:
        db_table = 'laboratory'


class SeedingType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)

    class Meta:
        db_table = 'seedingtype'


class Equipment(models.Model):
    id = models.AutoField(primary_key=True)
    equipmentid = models.IntegerField()
    type = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)

    class Meta:
        db_table = 'equipment'


class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'organization'


class Barn(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        db_table = 'barn'

class MilkingSystem(models.Model):
    id = models.AutoField(primary_key=True)
    equipment_id = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True)
    barn = models.ForeignKey(Barn, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        db_table = 'milking_system'


class Animal(models.Model):
    id = models.AutoField(primary_key=True)
    euid = models.CharField(unique=True, max_length=256)
    name = models.CharField(max_length=128)
    breed = models.ForeignKey(Breed, on_delete=models.SET_NULL, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    birthDate = models.DateField()
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


class Weight(models.Model):
    id = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField()
    weight = models.DecimalField(max_digits=8, decimal_places=3)
    automaticmeasurement = models.BooleanField()
    equipment_id = models.CharField(max_length=128, default="")

    class Meta:
        db_table = 'weight'


class Calving(models.Model):
    id = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    assistance = models.BooleanField()
    calvingnumber = models.IntegerField()

    class Meta:
        db_table = 'calving'


class Insemination(models.Model):
    id = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    bull = models.CharField(max_length=128)
    insemination_method = models.ForeignKey(SeedingType, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'insemination'


class PregnancyCheck(models.Model):
    id = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    result = models.BooleanField()
    calvingdate = models.DateField()

    class Meta:
        db_table = 'pregnancycheck'


class Feed(models.Model):
    id = models.AutoField(primary_key=True)
    feed_id = models.CharField(max_length=256)
    name = models.CharField(max_length=128)
    mixing_date = models.DateField()
    fresh_weight = models.DecimalField(max_digits=10, decimal_places=3)
    dry_matter_content = models.IntegerField()
    date = models.DateField()

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
    somatic_cell_count = models.IntegerField(null=True)
    colour = models.CharField(max_length=64, null=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    total_flow_duration = models.IntegerField(null=True)
    rf_flow_duration = models.IntegerField(null=True)
    rb_flow_duration = models.IntegerField(null=True)
    lf_flow_duration = models.IntegerField(null=True)
    lb_flow_duration = models.IntegerField(null=True)
    milking_system = models.ForeignKey(MilkingSystem, on_delete=models.SET_NULL, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'milking_event'