
from rest_framework import serializers
from finliveapp.models import Animal, Breed, Gender, Organization, Barn


class BreedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Breed
        fields = '__all__'


class GenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gender
        fields = '__all__'


class AnimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Animal
        fields = '__all__'
