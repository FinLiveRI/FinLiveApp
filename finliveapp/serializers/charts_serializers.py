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