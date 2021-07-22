
from django.shortcuts import get_object_or_404
from finliveapp.models import Organization, Breed, Gender, Barn
from finliveapp.serializers.management_serializer import OrganizationSerializer, BarnSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class OrganizationsView(APIView):
    # TODO add decorators
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        serializer = OrganizationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        # TODO check permissions
        user = request.user
        organizations = Organization.objects.all()
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)


class OrganizationView(APIView):
    # TODO add decorators
    def get(self, request, *args, **kwargs):
        # TODO check permissions
        user = request.user
        organization = get_object_or_404(Organization, id=kwargs['id'])
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        data = request.data
        organization = get_object_or_404(Organization, id=kwargs['id'])
        serializer = OrganizationSerializer(organization, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BarnsView(APIView):
    # TODO add decorators
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        serializer = BarnSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        # TODO check permissions
        user = request.user
        barns = Barn.objects.all()
        serializer = BarnSerializer(barns, many=True)
        return Response(serializer.data)
