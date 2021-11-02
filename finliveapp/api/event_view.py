from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404

from finliveapp.common.utils import dictTolist
from finliveapp.models import Animal, Calving, Organization, Milking_Event, Weight
from finliveapp.serializers.animal_serializers import CalvingSerializer
from finliveapp.serializers.milking_serializers import MilkingEventSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# TODO Milking event
# TODO Insemination event
# TODO pregnancy check event
# TODO weight event
from finliveapp.serializers.weight_serializers import WeightSerializer


class CalvingsView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        organization = get_object_or_404(Organization, id=organizationid)
        calvinglist = dictTolist(data)
        if not calvinglist:
            return Response({'error': "Calving data missing"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer = CalvingSerializer(data=calvinglist, organization=organization, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({'error': 'Errors in calving data'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        organization = get_object_or_404(Organization, id=organizationid)
        calving = Calving.objects.filter(organization=organization)
        serializer = CalvingSerializer(calving, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CalvingView(APIView):
    def get(self, request, *args, **kwargs):
        calving = get_object_or_404(Calving, id=kwargs['id'])
        serializer = CalvingSerializer(calving)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        calving = get_object_or_404(Calving, id=kwargs['id'])
        serializer = CalvingSerializer(calving, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MilkingEventsView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        organization = get_object_or_404(Organization, id=organizationid)
        milkinglist = dictTolist(data)
        if not milkinglist:
            return Response({'error': "Milking data missing"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer = MilkingEventSerializer(data=milkinglist, **{'editor': request.user,
                                                         'organization': organization}, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': "Saving milking data failed"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        organization = get_object_or_404(Organization, id=organizationid)
        milking = Milking_Event.objects.filter(organization=organization)
        serializer = MilkingEventSerializer(milking, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MilkingEventView(APIView):
    def get(self, request, *args, **kwargs):
        milking = get_object_or_404(Milking_Event, id=kwargs['id'])
        serializer = MilkingEventSerializer(milking)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        milking = get_object_or_404(Milking_Event, id=kwargs['id'])
        serializer = MilkingEventSerializer(milking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WeightingsView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        organization = get_object_or_404(Organization, id=organizationid)
        weightlist = dictTolist(data)
        if not weightlist:
            return Response({'error': "Weight data missing"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer = WeightSerializer(data=weightlist, **{'editor': request.user,
                                                         'organization': organization}, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': "Saving weight data failed"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        organization = get_object_or_404(Organization, id=organizationid)
        weighting = Weight.objects.filter(organization=organization)
        serializer = WeightSerializer(weighting, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WeightingEventView(APIView):
    def get(self, request, *args, **kwargs):
        weighting = get_object_or_404(Weight, id=kwargs['id'])
        serializer = MilkingEventSerializer(weighting)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        weighting = get_object_or_404(Milking_Event, id=kwargs['id'])
        serializer = WeightSerializer(weighting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)