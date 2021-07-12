from rest_framework import serializers
from finliveapp.models import Animal, Breed, Gender


class BreedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Breed


class GenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gender


class AnimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Animal
        fields = ['id', ]