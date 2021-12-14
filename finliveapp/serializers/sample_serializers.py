from datetime import datetime
from django.core.validators import EMPTY_VALUES
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from finliveapp.models import Animal, BloodSample, Organization, GasMeasurement, Equipment


class BloodSampleSerializer(serializers.ModelSerializer):

    class Meta:
        model = BloodSample
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop('editor', None)
        self.organization = kwargs.pop('organization', None)
        super(BloodSampleSerializer, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        _data = data
        if 'animalid' in _data:
            try:
                animal = Animal.objects.get(animalid=_data.get('animalid'), organization=self.organization)
                _data['animal'] = animal.id
                _data['euid'] = animal.euid
            except Exception:
                raise serializers.ValidationError({'animal': "Animalid mismatch"})
        elif 'euid' in _data:
            try:
                animal = Animal.objects.get(euid=_data.get('euid'), organization=self.organization)
                _data['animal'] = animal.id
                _data['euid'] = animal.euid
            except Exception:
                raise serializers.ValidationError({'animal': "Animalid mismatch"})
        if 'organization' in _data:
            try:
                if isinstance(data.get('organization'), str):
                    organization = get_object_or_404(Organization, id=self.organization,
                                                     name=_data.get('organization').lower())
                    data['organization'] = organization.id
                else:
                    data['organization'] = self.organization.id
            except Exception:
                raise serializers.ValidationError({'organization': "Organization mismatch"})
        if 'time_stamp' in _data:
            _datetime = datetime.strptime(data.get('time_stamp')[0:10], '%Y-%m-%d')
            _data['time_stamp'] = _datetime.date()

        return super().to_internal_value(_data)

    def create(self, validated_data):
        data = validated_data
        data['created_by'] = self.editor
        data['modified_by'] = self.editor
        return BloodSample.objects.create(**data)

    def update(self, instance, validated_data):
        data = validated_data
        data['modified_by'] = self.editor
        return super(BloodSampleSerializer, self).update(instance, data)


class GasSystemSerializer(serializers.ModelSerializer):

    class Meta:
        model = GasMeasurement
        fields = '__all__'

    def to_internal_value(self, data):
        _data = data
        animal = get_object_or_404(Animal, euid=data.get('euid'), organization=data.get('organization'))
        _data['animal'] = animal.id
        equipment = get_object_or_404(Equipment, equipmentid=data.get('equipmentid'))
        _data['equipment'] = equipment.id

        return super().to_internal_value(_data)

