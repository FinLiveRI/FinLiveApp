import csv
import json
from itertools import chain
from operator import attrgetter
from datetime import datetime, timedelta

from django.core.validators import EMPTY_VALUES
from django.db.models import Sum, Avg, F, When, Case, Value, ExpressionWrapper, IntegerField, Count
from django.db.models.functions import Trunc
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from finliveapp.models import Animal, Feeding, Weight, Milking_Event, Calving
from finliveapp.serializers.animal_serializers import AnimalSerializer, AnimalViewSerializer
from finliveapp.serializers.charts_serializers import VisitDurationSerializer, AnimalChartsSerializer, \
    DailyWeightSerializer, DailyMilkSerializer, DailyFeedingSerializer
from finliveapp.serializers.weight_serializers import WeightSerializer


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
            .values('day')\
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


class AnimalChartsView(APIView):
    def get(self, request, *args, **kwargs):
        organizationid = self.request.META.get('HTTP_X_ORG', None)

        data = {}
        result = {}

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
        #animalid = data.get('animalid')
        euid = data.get('euid')
        farmid = data.get('farmid')

        animal = get_object_or_404(Animal, euid=euid, organization_id=organizationid, barn__farmid=farmid)
        animalserializer = AnimalViewSerializer(animal)
        result['animal'] = animalserializer.data
        last_calving_date = Calving.objects.filter(animal=animal).order_by('-date').values('date').first()
        # feeding duration per day
        duration_per_day = Feeding.objects.filter(animal=animal, organization_id=organizationid,
                                                  visit_start_time__range=[begin, end])\
            .annotate(visit_day=Trunc('visit_start_time', 'day'))\
            .values('visit_day')\
            .annotate(duration=Sum('visit_duration'))

        durationserializer = VisitDurationSerializer(duration_per_day, calving=last_calving_date, many=True)
        result['duration'] = durationserializer.data

        # average animal weight per day
        averageweight = Weight.objects.filter(animal=animal, organization_id=organizationid,
                                              timestamp__range=[begin, end])\
            .annotate(day=Trunc('timestamp', 'day'))\
            .values('day')\
            .aggregate(daily_weight=Avg('weight'))
        weightserializer = DailyWeightSerializer(averageweight, calving=last_calving_date, many=True)
        result['weight'] = weightserializer.data

        # feed consumption per day
        feed_per_day = Feeding.objects.filter(animal=animal, organization_id=organizationid,
                                                  visit_start_time__range=[begin, end])\
            .annotate(day=Trunc('visit_start_time', 'day'))\
            .values('day')\
            .annotate(daily_weight=Sum('feed_weight'))
        feedserializer = DailyWeightSerializer(feed_per_day, calving=last_calving_date, many=True)
        result['feed'] = feedserializer.data

        milk_per_day = Milking_Event.objects.filter(animal=animal, organization_id=organizationid,
                                                    start_time__range=[begin, end])\
            .annotate(day=Trunc('start_time', 'day'))\
            .values('day')\
            .annotate(total_milk=Sum('total_milk_weight'))
        milkserializer = DailyMilkSerializer(milk_per_day, calving=last_calving_date, many=True)
        result['milk'] = milkserializer.data

        return Response(result, status=status.HTTP_200_OK)


class AnimalChart(APIView):

    def results_to_csv(self, chartdata, begin, end, filename="animalchart.csv"):
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename=%s' % filename},
        )

        writer = csv.writer(response)
        day = begin
        animal = chartdata.pop('animal')
        animalrow = []
        animalrow.append(animal.get('euid') if 'euid' in animal else '')
        animalrow.append(animal.get('animalid') if 'animalid' in animal else '')
        animalrow.append(animal.get('farmid') if 'farmid' in animal else '')
        animalrow.append(animal.get('parity') if 'parity' in animal else '')
        # calvingdate = animal.get('calvingdate') if 'calvingdate' in animal else None
        header = ['euid', 'animalid', 'farmid', 'parity', 'day',
                  'lactation', 'feed duration', 'feed weight', 'feeding count',
                  'weight', 'total milk', 'milking count']
        writer.writerow(header)
        feed = chartdata.get('feed')
        weight = chartdata.get('weight')
        milk = chartdata.get('milk')

        while day < end:
            newrow = animalrow.copy()
            newrow.append(day.strftime("%Y-%m-%d"))
            str_day = day.strftime("%Y-%m-%d")

            _feed = next((item for item in feed if item.get("day", None) == str_day), None)
            if _feed:
                newrow.append(_feed.get('lactation') if 'lactation' in _feed else '')
                newrow.append(_feed.get('duration') if 'duration' in _feed else '')
                newrow.append(_feed.get('daily_weight') if 'daily_weight' in _feed else '')
                newrow.append(_feed.get('visit_count') if 'visit_count' in _feed else '')
            else:
                newrow.extend(['', '', ''])

            _weight = next((item for item in weight if item.get("day", None) == str_day), None)
            if _weight:
                newrow.append(_weight.get('weight') if 'weight' in _weight else '')
            else:
                newrow.append('')

            _milk = next((item for item in milk if item.get("day", None) == str_day), None)
            if _milk:
                newrow.append(_milk.get('total_milk') if 'total_milk' in _milk else '')
                newrow.append(_milk.get('visit_count') if 'visit_count' in _milk else '')
            else:
                newrow.extend(['', ''])

            writer.writerow(newrow)
            day += timedelta(days=1)
        return response

    def get(self, request, *args, **kwargs):
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        data = {}
        result = {}
        filter = self.request.META.get('HTTP_X_FILTER', None)
        if filter:
            data = json.loads(filter)
        try:
            begin = datetime.strptime(data.get('begin'), "%Y-%m-%d")
            end = datetime.strptime(data.get('end'), "%Y-%m-%d") + timedelta(days=1)
            filetype = data.get('download', None)
        except Exception:
            return Response({'date': "Invalid date value"}, status=status.HTTP_400_BAD_REQUEST)
        if begin > end:
            return Response({'date': "Invalid date range"}, status=status.HTTP_400_BAD_REQUEST)
        animalid = data.get('animalid')

        # animal information
        animal = get_object_or_404(Animal, animalid=animalid, organization_id=organizationid)
        animalserializer = AnimalViewSerializer(animal)
        last_calving_date = Calving.objects.filter(animal=animal).order_by('-date').values('date', 'parity').first()
        _animal = animalserializer.data
        _animal['parity'] = last_calving_date.pop('parity') if 'parity' in last_calving_date else 0
        _animal['farmid'] = animal.barn.farmid
        result['animal'] = _animal

        # average animal weight per day
        averageweight = Weight.objects.filter(animal=animal, organization_id=organizationid,
                                              timestamp__range=[begin, end])\
            .annotate(day=Trunc('timestamp', 'day'))\
            .values('day')\
            .aggregate(daily_weight=Avg('weight'))
        weightserializer = DailyWeightSerializer(averageweight, calving=last_calving_date, many=True)
        result['weight'] = weightserializer.data

        # feed consumption per day
        feed_per_day = Feeding.objects.filter(animal=animal, organization_id=organizationid,
                                                  visit_start_time__range=[begin, end])\
            .annotate(day=Trunc('visit_start_time', 'day'))\
            .values('day')\
            .annotate(daily_weight=Sum('feed_weight'), visit_count=Count('feed_weight'), duration=Sum('visit_duration'))
        feedserializer = DailyFeedingSerializer(feed_per_day, calving=last_calving_date, many=True)
        result['feed'] = feedserializer.data

        milk_per_day = Milking_Event.objects.filter(animal=animal, organization_id=organizationid,
                                                    start_time__range=[begin, end])\
            .annotate(day=Trunc('start_time', 'day'))\
            .values('day')\
            .annotate(total_milk=Sum('total_milk_weight'), visit_count=Count('total_milk_weight'))
        milkserializer = DailyMilkSerializer(milk_per_day, calving=last_calving_date, many=True)
        result['milk'] = milkserializer.data

        return self.results_to_csv(result, begin, end)



