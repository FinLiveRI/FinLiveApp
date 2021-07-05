from django.contrib.auth.models import User
from django.db import models


class Breed(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'breed'


class Gender(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'gender'


class SeedingType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256)

    class Meta:
        db_table = 'seedingtype'


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


class Animal(models.Model):
    id = models.AutoField(primary_key=True)
    euid = models.CharField(unique=True, max_length=256)
    name = models.CharField(max_length=128)
    breed = models.ForeignKey(Breed, on_delete=models.SET_NULL, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    birthDate = models.DateField()
    animalid = models.CharField(max_length=128)
    barn = models.ForeignKey(Barn, on_delete=models.SET_NULL, null=True)
    arrivaldate = models.DateField()
    departuredate = models.DateField(null=True, blank=True)
    departurereason = models.CharField(max_length=256, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'animal'


class Weight(models.Model):
    id = models.AutoField(primary_key=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField()
    weight = models.DecimalField(max_digits=8, decimal_places=3)
    automaticmeasurement = models.BooleanField()

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
    inseminationmethod = models.ForeignKey(SeedingType, on_delete=models.SET_NULL, null=True)

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
