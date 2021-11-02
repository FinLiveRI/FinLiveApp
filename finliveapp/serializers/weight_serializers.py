from datetime import datetime
from django.core.validators import EMPTY_VALUES
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from finliveapp.models import Weight, Animal


class WeightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Weight
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop('editor', None)
        self.organization = kwargs.pop('organization', None)
        super(WeightSerializer, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if 'euid' in data:
            animal = Animal.objects.get(euid=data.get('euid'), organization=self.organization)
            data['animal'] = animal.id
        if self.organization:
            data['organization'] = self.organization.id
        if 'timestamp' in data:
            _datetime = datetime.strptime(data.get('timestamp')[0:10], '%Y-%m-%d')
            data['timestamp'] = _datetime.date()
        if 'automaticmeasurement' in data:
            if data.get('automaticmeasurement') in EMPTY_VALUES:
                data['automaticmeasurement'] = False

        result = super().to_internal_value(data)
        return result

    def create(self, validated_data):
        data = validated_data
        data['created_by'] = self.editor
        data['modified_by'] = self.editor
        return Weight.objects.create(**data)

    def update(self, instance, validated_data):
        data = validated_data
        data['modified_by'] = self.editor
        return super(WeightSerializer, self).update(instance, data)
