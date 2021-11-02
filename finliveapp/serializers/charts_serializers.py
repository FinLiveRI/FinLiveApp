from datetime import datetime, date
from django.core.validators import EMPTY_VALUES
from rest_framework import serializers


class VisitDurationSerializer(serializers.Serializer):
    date = serializers.DateField(required=True)
    duration = serializers.IntegerField()

    class Meta:
        fields = ('date', 'duration')

    def to_representation(self, instance):
        instance['date'] = instance['date'].date()
        data = super(VisitDurationSerializer, self).to_representation(instance)
        data['duration'] = data.get('duration') // 60
        return data


class DailyWeightSerializer(serializers.Serializer):
    date = serializers.DateField(required=True)
    average = serializers.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        fields = ('date', 'average')

    def to_representation(self, instance):
        instance['date'] = instance['date'].date()
        data = super(DailyWeightSerializer, self).to_representation(instance)
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
        #fields = ('date', 'weight_average', 'daily_duration')

    def to_representation(self, instance):
        instance['day'] = instance['day'].date()
        data = super(AnimalChartsSerializer, self).to_representation(instance)
        data['daily_duration'] = data.get('daily_duration', 0) // 60
        return data