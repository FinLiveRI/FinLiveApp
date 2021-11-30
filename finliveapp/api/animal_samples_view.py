from django.shortcuts import get_object_or_404

from finliveapp.common.utils import dictTolist
from finliveapp.decorators.access import check_user_or_apikey
from finliveapp.models import Organization, BloodSample, GasSystem
from finliveapp.serializers.sample_serializers import BloodSampleSerializer, GasSystemSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class BloodSamplesView(APIView):
    @check_user_or_apikey()
    def post(self, request, *args, **kwargs):
        data = request.data
        user = None if request.user.is_anonymous else request.user
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        organization = get_object_or_404(Organization, id=organizationid)
        result = []
        samplelist = dictTolist(data)
        if not samplelist:
            return Response({'error': "Blood sample data missing"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer = BloodSampleSerializer(data=samplelist, **{'editor': user,
                                                         'organization': organization}, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': "Saving blood sample data failed"}, status=status.HTTP_400_BAD_REQUEST)

    @check_user_or_apikey()
    def get(self, request, *args, **kwargs):
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        organization = get_object_or_404(Organization, id=organizationid)
        samples = BloodSample.objects.filter(organization=organization)
        serializer = BloodSampleSerializer(samples, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BloodSampleView(APIView):
    @check_user_or_apikey()
    def get(self, request, *args, **kwargs):
        bloodsample = get_object_or_404(BloodSample, id=kwargs['id'])
        serializer = BloodSampleSerializer(bloodsample)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @check_user_or_apikey()
    def put(self, request, *args, **kwargs):
        weighting = get_object_or_404(BloodSample, id=kwargs['id'])
        user = None if request.user.is_anonymous else request.user
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        organization = get_object_or_404(Organization, id=organizationid)
        serializer = BloodSampleSerializer(weighting, data=request.data, **{'editor': user,
                                                         'organization': organization}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GasSystemsView(APIView):
    @check_user_or_apikey()
    def post(self, request, *args, **kwargs):
        data = request.data
        samplelist = dictTolist(data)
        if not samplelist:
            return Response({'error': "Gas data missing"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer = GasSystemSerializer(data=samplelist, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'error': "Saving gas data failed"}, status=status.HTTP_400_BAD_REQUEST)

    @check_user_or_apikey()
    def get(self, request, *args, **kwargs):
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        organization = get_object_or_404(Organization, id=organizationid)
        gas = GasSystem.objects.filter(organization=organization)
        serializer = GasSystemSerializer(gas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
