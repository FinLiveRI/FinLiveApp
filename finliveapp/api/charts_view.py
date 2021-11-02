import json
from itertools import chain
from operator import attrgetter
from datetime import datetime, timedelta

from django.db.models import Sum, Avg
from django.db.models.functions import Trunc
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# filter duration daily
# a = Feeding.objects.filter(animal_id=7, visit_start_time__range=[datetime(2021, 3, 30), datetime(2021, 4, 1)])
#                       .annotate(visit_start=Trunc('visit_start_time', 'day'))
#                       .values('visit_start')
#                       .annotate(sum=Sum('visit_duration'))
from django.shortcuts import get_object_or_404
from finliveapp.models import Animal, Feeding, Weight, Milking_Event
from finliveapp.serializers.charts_serializers import VisitDurationSerializer, AnimalChartsSerializer


class FeedingDuration(APIView):

    def get(self, request, *args, **kwargs):
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        data = {}
        filter = self.request.META.get('HTTP_X_FILTER', None)
        if filter:
            data = json.loads(filter)
        try:
            begin = datetime.strptime(data.get('begin'), "%Y-%m-%d")
            end = datetime.strptime(data.get('end'), "%Y-%m-%d") + timedelta(days=1)
        except Exception:
            return Response({'date': "Invalid date value"}, status=status.HTTP_400_BAD_REQUEST)
        if begin > end:
            return Response({'date': "Invalid date range"}, status=status.HTTP_400_BAD_REQUEST)
        animalid = data.get('animalid')
        duration_per_day = Feeding.objects.filter(animal_id=animalid, organization_id=organizationid,
                                                  visit_start_time__range=[begin, end])\
            .annotate(visit_day=Trunc('visit_start_time', 'day'))\
            .values('date')\
            .annotate(duration=Sum('visit_duration'))

        serializer = VisitDurationSerializer(duration_per_day, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FeedingDailyAmount(APIView):

    def get(self, request, *args, **kwargs):
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        data = {}
        filter = self.request.META.get('HTTP_X_FILTER', None)
        if filter:
            data = json.loads(filter)
        try:
            begin = datetime.strptime(data.get('begin'), "%Y-%m-%d")
            end = datetime.strptime(data.get('end'), "%Y-%m-%d") + timedelta(days=1)
        except Exception:
            return Response({'date': "Invalid date value"}, status=status.HTTP_400_BAD_REQUEST)
        if begin > end:
            return Response({'date': "Invalid date range"}, status=status.HTTP_400_BAD_REQUEST)

        animalid = data.get('animalid')


class AnimalCharts(APIView):

    def get(self, request, *args, **kwargs):
        result = {}
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        data = {}
        filter = self.request.META.get('HTTP_X_FILTER', None)
        if filter:
            data = json.loads(filter)
        try:
            begin = datetime.strptime(data.get('begin'), "%Y-%m-%d")
            end = datetime.strptime(data.get('end'), "%Y-%m-%d") + timedelta(days=1)
        except Exception:
            return Response({'date': "Invalid date value"}, status=status.HTTP_400_BAD_REQUEST)
        if begin > end:
            return Response({'date': "Invalid date range"}, status=status.HTTP_400_BAD_REQUEST)
        animalid = data.get('animalid')
        animal = get_object_or_404(Animal, animalid=animalid, organization_id=organizationid)
        duration_per_day = Feeding.objects.filter(animal=animal, organization_id=organizationid,
                                                  visit_start_time__range=[begin, end])\
            .annotate(day=Trunc('visit_start_time', 'day'))\
            .values('day')\
            .annotate(duration=Sum('visit_duration'))

        averageweight = Weight.objects.filter(animal=animal, organization_id=organizationid,
                                              timestamp__range=[begin, end])\
            .annotate(day=Trunc('timestamp', 'day'))\
            .values('day')\
            .aggregate(daily_weight=Avg('weight'))

        daily_milk = Milking_Event.objects.filter(animal=animal, organization_id=organizationid,
                                                  start_time__range=[begin, end])\
            .annotate(day=Trunc('start_time', 'day'))\
            .values('day')\
            .annotate(daily_milk=Sum('total_milk_weight'))
        resultlist = []

        while begin <= end:
            daily_values = animal.__dict__
            daily_values['day'] = begin
            resultlist.append(daily_values)
            begin += timedelta(days=1)

        # result_list = sorted(chain(duration_per_day, daily_milk), key=lambda instance: instance.day) #key=attrgetter('day'))
        serializer = AnimalChartsSerializer(resultlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)