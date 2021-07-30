from datetime import datetime
from django.core.validators import EMPTY_VALUES
from rest_framework import serializers
from finliveapp.models import Animal, Breed, Gender, Organization, Barn, Calving
from finliveapp.serializers.management_serializer import BarnSerializer, UserAccountSerializer, OrganizationSerializer


class BreedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Breed
        fields = '__all__'


class GenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gender
        fields = '__all__'


class AnimalSerializer(serializers.ModelSerializer):
    barn = BarnSerializer(read_only=True)
    breed = BreedSerializer(read_only=True)
    gender = GenderSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    created_by = UserAccountSerializer(read_only=True)
    modified_by = UserAccountSerializer(read_only=True)

    class Meta:
        model = Animal
        fields = ['id', 'euid', 'name', 'birthdate', 'animalid', 'arrivaldate', 'departuredate', 'departurereason',
                  'created', 'modified', 'barn', 'breed', 'gender', 'organization', 'created_by', 'modified_by']
        read_only_fields = ['id', 'created', 'modified', 'created_by', 'modified_by']


class NewAnimalSerializer(serializers.Serializer):
    euid = serializers.CharField(allow_blank=False, max_length=256)
    name = serializers.CharField(allow_blank=False, max_length=128)
    birthdate = serializers.DateField()
    animalid = serializers.IntegerField()
    rfid = serializers.CharField(max_length=256, required=False)
    arrivaldate = serializers.DateField(required=False)
    departuredate = serializers.DateField(required=False)
    departurereason = serializers.CharField(max_length=256, allow_blank=True, required=False)

    def validate(self, attrs):
        data = serializers.Serializer.validate(self, attrs)
        return data


class CalvingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calving
        fields = '__all__'

    def __init__(self, organization=None, *args, **kwargs):
        self.organization = organization
        super(CalvingSerializer, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if 'euid' in data:
            animal = Animal.objects.get(euid=data.get('euid'), organization=self.organization)
            data['animal'] = animal.id
        if self.organization:
            data['organization'] = self.organization.id
        if 'date' in data:
            _datetime = datetime.strptime(data.get('date')[0:10], '%Y-%m-%d')
            data['date'] = _datetime.date()
        if 'assistance' in data:
            if data.get('assistance') in EMPTY_VALUES:
                data['assistance'] = ''

        result = super().to_internal_value(data)
        return result
