from datetime import datetime
from django.core.validators import EMPTY_VALUES
from django.shortcuts import get_object_or_404
from finliveapp.models import Feed, FeedAnalysis, Feeding, Organization, Barn, Animal, Equipment

from rest_framework import serializers


class FeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feed
        fields = '__all__'
        read_only_fields = ('id', 'created', 'modified')


class FeedingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feeding
        fields = '__all__'
        read_only_fields = ('id', 'created', 'modified')

    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop('editor', None)
        self.organization = kwargs.pop('organization', None)
        super(FeedingSerializer, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if 'visitstarttime' in data:
            data['visit_start_time'] = data.pop('visitstarttime')
        if 'visitendtime' in data:
            data['visit_end_time'] = data.pop('visitendtime')
        if 'visitduration' in data:
            data['visit_duration'] = data.pop('visitduration')
        if 'feedweight' in data:
            data['feed_weight'] = data.pop('feedweight')
        if 'feedconsumption' in data:
            data['feed_consumption'] = data.pop('feedconsumption')
        if 'equipmentid' in data:
            data['equipment_id'] = data.pop('equipmentid')
        if 'equipment_id' in data:
            try:
                data['equipment'] = Equipment.objects.get(equipmentid=data.get('equipment_id')).id
            except Exception:
                raise serializers.ValidationError({'equipment': "Equipment mismatch"})
        if 'organization' in data:
            try:
                if isinstance(data.get('organization'), str):
                    organization = get_object_or_404(Organization, id=self.organization,
                                                     name=data.get('organization').lower())
                    data['organization'] = organization.id
                else:
                    data['organization'] = self.organization
            except Exception:
                raise serializers.ValidationError({'organization': "Organization mismatch"})
        if 'animalid' in data:
            try:
                animal = get_object_or_404(Animal, animalid=data.get('animalid'), organization_id=data.get('organization'))
                data['animal'] = animal.id
            except Exception:
                raise serializers.ValidationError({'animal': "Animalid mismatch"})
        if 'farmid' in data:
            try:
                barn = get_object_or_404(Barn, farmid=data.get('farmid'), organization_id=data.get('organization'))
                data['barn'] = barn.id
            except Exception:
                raise serializers.ValidationError({'barn': "Farmid mismatch"})

        if 'feedid' in data:
            try:
                feed = get_object_or_404(Feed, feedid=data.get('feedid'), organization_id=data.get('organization'))
                data['feed'] = feed.id
            except Exception:
                raise serializers.ValidationError({'feed': "Feedid mismatch"})

        return super().to_internal_value(data)

    def create(self, validated_data):
        data = validated_data
        data['created_by'] = self.editor
        data['modified_by'] = self.editor
        return Feeding.objects.create(**data)

    def update(self, instance, validated_data):
        data = validated_data
        data['modified_by'] = self.editor
        return super(FeedingSerializer, self).update(instance, data)
