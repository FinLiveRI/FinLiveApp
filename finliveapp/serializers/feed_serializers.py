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


# Fast serializer for bulk creation of objects (5x speedup)
# all events needs to be from same farm and organization
class BulkFeedingSerializer(object):
    def __init__(self, data, organizationid, farmid):
        self.organizationid = organizationid
        self.data = data
        self.farmid = farmid
        self.fields = ('equipment', 'animal', 'start_time', 'end_time',
                  'visit_duration', 'feed_weight', 'feed_consumption', 'feed_name', 'organization', 'barn')

    def bulk_create(self):
        animals = Animal.objects.filter(barn__farmid=self.farmid).all()
        equipment = Equipment.objects.filter(barn__farmid=self.farmid).all()
        barn = Barn.objects.get(farmid=self.farmid)
        org = Organization.objects.get(id=self.organizationid)
        events = []
        for visit in self.data:
            visit["animal"] = animals.get(euid=visit["euid"])
            visit["equipment"] = equipment.get(equipmentid=visit["equipmentid"])
            visit["barn"] = barn
            visit["organization"] = org
            events.append(Feeding(**{f: visit[f] for f in self.fields}))
        fd = Feeding.objects.bulk_create(events, batch_size=1000)
        return True


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
            data['start_time'] = data.pop('visitstarttime')
        if 'visitendtime' in data:
            data['end_time'] = data.pop('visitendtime')
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

        if 'euid' in data:
            try:
                animal = get_object_or_404(Animal, euid=data.get('euid'), organization_id=data.get('organization'))
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

    def to_representation(self, instance):
        data = super(FeedingSerializer, self).to_representation(instance)
        if 'barn' in data:
            farm = Barn.objects.get(pk=data.pop('barn'))
            data['farmid'] = farm.farmid

        return data

    def create(self, validated_data):
        data = validated_data
        data['created_by'] = self.editor
        data['modified_by'] = self.editor

        feeding, created = Feeding.objects.update_or_create(
            animal_id=data.get('animal', None), visit_start_time=data.get('start_time', None),
            defaults=data)

        return feeding

    def update(self, instance, validated_data):
        data = validated_data
        data['modified_by'] = self.editor
        return super(FeedingSerializer, self).update(instance, data)


class NewFeedingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeding
        fields = ['id', 'start_time', 'end_time', 'visit_duration', 'feed_weight', 'feed_consumption',
                  'animal', 'equipment', 'feed', 'organization', 'created', 'created_by', 'modified', 'modified_by',
                  'barn']
        read_only_fields = ('id', 'created', 'modified')

    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop('editor', None)
        self.organization = kwargs.pop('organization', None)
        super(NewFeedingSerializer, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if 'visitstarttime' in data:
            data['start_time'] = data.pop('visitstarttime')
        if 'visitendtime' in data:
            data['end_time'] = data.pop('visitendtime')
        if 'visitduration' in data:
            data['visit_duration'] = data.pop('visitduration')
        if 'feedweight' in data:
            data['feed_weight'] = data.pop('feedweight')
        if 'feedconsumption' in data:
            data['feed_consumption'] = data.pop('feedconsumption')
        if 'equipmentid' in data:
            try:
                data['equipment'] = Equipment.objects.get(equipmentid=data.get('equipmentid')).id
            except Exception:
                raise serializers.ValidationError({'equipment': "Equipment mismatch"})
        if 'organization' in data:
            try:
                if isinstance(data.get('organization'), str):
                    organization = get_object_or_404(Organization, id=self.organization,
                                                     name=data.get('organization').lower())
                    data['organization'] = organization.id
                else:
                    data['organization_id'] = self.organization
            except Exception:
                raise serializers.ValidationError({'organization': "Organization mismatch"})

        if 'euid' in data:
            try:
                animal = get_object_or_404(Animal, euid=data.get('euid'), organization=data.get('organization'))
                data['animal'] = animal.id
            except Exception:
                raise serializers.ValidationError({'animal': "Animalid mismatch"})
        if 'farmid' in data:
            try:
                barn = get_object_or_404(Barn, farmid=data.get('farmid'), organization=data.get('organization'))
                data['barn'] = barn.id
            except Exception:
                raise serializers.ValidationError({'barn': "Farmid mismatch"})

        if 'feedid' in data:
            try:
                feed = get_object_or_404(Feed, feedid=data.get('feedid'), organization=data.get('organization'))
                data['feed'] = feed.id
            except Exception:
                raise serializers.ValidationError({'feed': "Feedid mismatch"})

        return super().to_internal_value(data)

    def to_representation(self, instance):
        data = super(NewFeedingSerializer, self).to_representation(instance)
        excluded = ['id', 'created', 'created_by', 'modified', 'modified_by']
        for field in excluded:
            del data[field]
        if 'barn' in data:
            farm = Barn.objects.get(pk=data.pop('barn'))
            data['farmid'] = farm.farmid
        animal = Animal.objects.get(pk=data.pop('animal'))
        data['animalid'] = animal.animalid
        data.move_to_end('animalid', last=False)
        data['euid'] = animal.euid
        data.move_to_end('euid', last=False)
        return data

    def create(self, validated_data):
        data = validated_data
        data['created_by'] = self.editor
        data['modified_by'] = self.editor

        feeding, created = Feeding.objects.update_or_create(
            animal=data.get('animal', None), visit_start_time=data.get('start_time', None),
            defaults=data)

        return feeding

    def update(self, instance, validated_data):
        data = validated_data
        data['modified_by'] = self.editor
        return super(NewFeedingSerializer, self).update(instance, data)
