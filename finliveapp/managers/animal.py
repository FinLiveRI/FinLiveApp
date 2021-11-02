from collections import OrderedDict
from django.db import models

from finliveapp.models import Animal


class AnimalFilter():

    def __init__(self, euid=None, name=None, birthdate=None, animalid=None, arrivaldate=None, departuredate=None,
                 departurereason=None, rfid=None, barn=None, organization=None, breed=None, gender=None):
        self.euid = euid
        self.name = name
        self.birthdate = birthdate
        self.animalid = animalid
        self.arrivaldate = arrivaldate
        self.departuredate = departuredate
        self.departurereason = departurereason
        self.rfid = rfid
        self.barn = barn
        self.organization = organization
        self.breed = breed
        self.gender = gender

    def pick_filters(self, data):

        if 'euid' in data:
            self.euid = data.get('euid')
        if 'name' in data:
            self.name = data.get('name')
        if 'birthdate' in data:
            self.birthdate = data.get('birthdate')
        if 'animalid' in data:
            self.animalid = data.get('animalid')
        if 'arrivaldate' in data:
            self.arrivaldate = data.get('arrivaldate')
        if 'departuredate' in data:
            self.departuredate = data.get('departuredate')
        if 'departurereason' in data:
            self.departurereason = data.get('departurereason')
        if 'rfid' in data:
            self.rfid = data.get('rfid')
        if 'barn' in data:
            self.barn = data.get('barn')
        if 'organization' in data:
            self.organization = data.get('organization')
        if 'breed' in data:
            self.breed = data.get('breed')
        if 'gender' in data:
            self.gender = data.get('gender')


class AnimalManager(models.Manager):

    def get_animals(self, data):
        animals = None
        filters = AnimalFilter()
        filters.pick_filters(data)

        kwargs = OrderedDict()

        if filters.animalid:
            kwargs['animalid'] = filters.animalid
        if filters.name:
            kwargs['{0}__{1}'.format('name', 'icontains')] = filters.name
        if filters.rfid:
            kwargs['rfid'] = filters.rfid
        if filters.euid:
            kwargs['euid'] = filters.euid
        if filters.birthdate:
            kwargs['birthdate'] = filters.birthdate
        if filters.arrivaldate:
            kwargs['arrivaldate'] = filters.arrivaldate
        if filters.departuredate:
            kwargs['departuredate'] = filters.departuredate
        if filters.departurereason:
            kwargs['departurereason'] = filters.departurereason
        if filters.organization:
            kwargs['organization'] = filters.organization
        if filters.breed:
            kwargs['breed'] = filters.breed
        if filters.gender:
            kwargs['gender'] = filters.gender
        if filters.barn:
            kwargs['barn_id'] = filters.barn
        try:
            if 'animalid' in kwargs:
                animals = Animal.objects.get(**kwargs)
            else:
                animals = Animal.objects.filter(**kwargs)

        except Animal.DoesNotExist:
            animals = None

        return animals
