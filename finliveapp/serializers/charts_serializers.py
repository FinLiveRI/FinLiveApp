from datetime import datetime, date
from django.core.validators import EMPTY_VALUES
from rest_framework import serializers


class VisitDurationSerializer(serializers.Serializer):
    visit_day = serializers.DateField(required=True)
    duration = serializers.IntegerField()

    class Meta:
        fields = ('visit_day', 'duration')

    def __init__(self, *args, **kwargs):
        self.calving = kwargs.pop('calving', None)
        super(VisitDurationSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, instance):
        if isinstance(instance, dict):
            instance['visit_day'] = instance['visit_day'].date()
            data = super(VisitDurationSerializer, self).to_representation(instance)
            data['duration'] = data.get('duration') // 60
            if self.calving not in EMPTY_VALUES:
                data['lactation'] = abs(instance['visit_day']-self.calving.get('date')).days
            else:
                data['lactation'] = None
        else:
            data = {}
        return data


class DailyWeightSerializer(serializers.Serializer):
    day = serializers.DateField(required=True)
    daily_weight = serializers.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        fields = ('day', 'daily_weight')

    def __init__(self, *args, **kwargs):
        self.calving = kwargs.pop('calving', None)
        super(DailyWeightSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, instance):
        if isinstance(instance, dict):
            instance['day'] = instance['day'].date()
            data = super(DailyWeightSerializer, self).to_representation(instance)
            if self.calving not in EMPTY_VALUES:
                data['lactation'] = abs(instance['day'] - self.calving.get('date')).days
            else:
                data['lactation'] = None
        else:
            data = {}
        return data


class DailyMilkSerializer(serializers.Serializer):
    day = serializers.DateField(required=True)
    total_milk = serializers.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        fields = ('day', 'total_milk')

    def __init__(self, *args, **kwargs):
        self.calving = kwargs.pop('calving', None)
        super(DailyMilkSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, instance):
        if isinstance(instance, dict):
            instance['day'] = instance['day'].date()
            data = super(DailyMilkSerializer, self).to_representation(instance)
            if self.calving not in EMPTY_VALUES:
                data['lactation'] = abs(instance['day'] - self.calving.get('date')).days
            else:
                data['lactation'] = None
        else:
            data = {}
        return data


class DailyFeedingSerializer(serializers.Serializer):
    day = serializers.DateField(required=True)
    daily_weight = serializers.DecimalField(max_digits=8, decimal_places=3)
    visit_count = serializers.IntegerField()
    duration = serializers.IntegerField()

    class Meta:
        fields = ('day', 'daily_weight', 'visit_count', 'duration')

    def __init__(self, *args, **kwargs):
        self.calving = kwargs.pop('calving', None)
        super(DailyFeedingSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, instance):
        if isinstance(instance, dict):
            instance['day'] = instance['day'].date()
            data = super(DailyFeedingSerializer, self).to_representation(instance)
            if self.calving not in EMPTY_VALUES:
                data['lactation'] = abs(instance['day'] - self.calving.get('date')).days
            else:
                data['lactation'] = None
        else:
            data = {}
        return data


class AnimalChartsSerializer(serializers.Serializer):
    day = serializers.DateField(required=True)
    #weight_average = serializers.DecimalField(max_digits=8, decimal_places=3)
    daily_duration = serializers.IntegerField()
    animalid = serializers.IntegerField()
    euid = serializers.CharField()
    farmid = serializers.IntegerField()

    class Meta:
        fields = ('animalid', 'euid', 'farmid', 'day', 'weight_average', 'daily_duration')

    def to_representation(self, instance):
        instance['day'] = instance['day'].date()
        data = super(AnimalChartsSerializer, self).to_representation(instance)
        data['daily_duration'] = data.get('daily_duration', 0) // 60
        return data