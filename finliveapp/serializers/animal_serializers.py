
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