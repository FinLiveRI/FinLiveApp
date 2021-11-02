
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from finliveapp.models import Organization, Barn, Milking_Event, MilkingSystem
from finliveapp.managers.animal import AnimalManager


class MilkingEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Milking_Event
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop('editor', None)
        self.organization = kwargs.pop('organization', None)
        super(MilkingEventSerializer, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if 'organization' in data:
            organization = get_object_or_404(Organization, id=self.organization.id, name=data.get('organization').lower())
            data['organization'] = organization.id
        if 'farmid' in data:
            barn = get_object_or_404(Barn, farmid=data.get('farmid'), organization=self.organization)
            data['barn'] = barn.id
        if 'milking_system' in data:
            system = get_object_or_404(MilkingSystem, equipment__name=data.get('milking_system'), organization=self.organization)
            data['milking_system'] = system.id
        if 'animalid' in data:
            animal = AnimalManager().get_animals(data)
            if animal:
                data['animal'] = animal.id
            else:
                raise serializers.ValidationError({'animal': "Animal mismatch"})

        return super(MilkingEventSerializer, self).to_internal_value(data)

    def create(self, validated_data):
        data = validated_data
        data['created_by'] = self.editor
        data['modified_by'] = self.editor
        return Milking_Event.objects.create(**data)

    def update(self, instance, validated_data):
        data = validated_data
        data['modified_by'] = self.editor
        return super(MilkingEventSerializer, self).update(instance, data)
