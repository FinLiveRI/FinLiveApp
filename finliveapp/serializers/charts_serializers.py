from datetime import datetime, date
from django.core.validators import EMPTY_VALUES
from rest_framework import serializers


class VisitDurationSerializer(serializers.Serializer):
    visit_day = serializers.DateField(required=True)
    duration = serializers.IntegerField()

    class Meta:
        fields = ('visit_day', 'duration')

    def to_representation(self, instance):
        instance['visit_day'] = instance['visit_day'].date()
        data = super(VisitDurationSerializer, self).to_representation(instance)
        data['duration'] = data.get('duration') // 60
        return data


class DailyWeightSerializer(serializers.Serializer):
    day = serializers.DateField(required=True)
    daily_weight = serializers.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        fields = ('day', 'daily_weight')

    def to_representation(self, instance):
        if isinstance(instance, dict):
            instance['day'] = instance['day'].date()
            data = super(DailyWeightSerializer, self).to_representation(instance)
        else:
            data = {}
        return data


class DailyMilkSerializer(serializers.Serializer):
    day = serializers.DateField(required=True)
    total_milk = serializers.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        fields = ('day', 'total_milk')

    def to_representation(self, instance):
        if isinstance(instance, dict):
            instance['day'] = instance['day'].date()
            data = super(DailyMilkSerializer, self).to_representation(instance)
        else:
            data = {}
        return data


class AnimalChartsSerializer(serializers.Serializer):
    day = serializers.DateField(required=True)
    weight_average = serializers.DecimalField(max_digits=8, decimal_places=3)
    daily_duration = serializers.IntegerField()
    #animalid = serializers.IntegerField()
    #euid = serializers.CharField()
    #farmid = serializers.IntegerField()

    class Meta:
        fields = ('animalid', 'euid', 'farmid', 'day', 'weight_average', 'daily_duration')

    def to_representation(self, instance):
        instance['day'] = instance['day'].date()
        data = super(AnimalChartsSerializer, self).to_representation(instance)
        data['daily_duration'] = data.get('daily_duration', 0) // 60
        return data