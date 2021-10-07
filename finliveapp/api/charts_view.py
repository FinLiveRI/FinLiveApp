from datetime import datetime, timedelta

from django.db.models import Sum
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
from finliveapp.models import Animal, Feeding
from finliveapp.serializers.charts_serializers import VisitDurationSerializer


class FeedingDuration(APIView):

    def get(self, request, *args, **kwargs):
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        data = request.data
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
            .values('visit_day')\
            .annotate(duration=Sum('visit_duration'))

        serializer = VisitDurationSerializer(duration_per_day, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class FeedingDailyAmount(APIView):

    def get(self, request, *args, **kwargs):
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        data = request.data
        try:
            begin = datetime.strptime(data.get('begin'), "%Y-%m-%d")
            end = datetime.strptime(data.get('end'), "%Y-%m-%d") + timedelta(days=1)
        except Exception:
            return Response({'date': "Invalid date value"}, status=status.HTTP_400_BAD_REQUEST)
        if begin > end:
            return Response({'date': "Invalid date range"}, status=status.HTTP_400_BAD_REQUEST)

        animalid = data.get('animalid')
