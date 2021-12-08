
from django.shortcuts import get_object_or_404
from finliveapp.decorators.access import check_user_organization, check_user_or_apikey
from finliveapp.models import Barn, MilkingSystem, Organization, Equipment, Laboratory
from finliveapp.serializers.management_serializer import OrganizationSerializer, BarnSerializer, \
    MilkingsystemSerializer, EquipmentSerializer, LaboratorySerializer
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
    @check_user_organization()
    def post(self, request, *args, **kwargs):
        data = request.data
        user = None if request.user.is_anonymous else request.user
        serializer = BarnSerializer(data=data, **{'editor': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_user_organization()
    def get(self, request, *args, **kwargs):
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        barns = Barn.objects.filter(organization_id=organizationid)
        serializer = BarnSerializer(barns, many=True)
        return Response(serializer.data)


class BarnView(APIView):
    def get(self, request, *args, **kwargs):
        barn = get_object_or_404(Barn, id=kwargs['id'])
        serializer = BarnSerializer(barn)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        barn = get_object_or_404(Barn, id=kwargs['id'])
        user = None if request.user.is_anonymous else request.user
        serializer = BarnSerializer(barn, data=request.data, **{'editor': user}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MilkingSystemsView(APIView):
    # TODO add decorators
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        serializer = MilkingsystemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        milkingsystems = MilkingSystem.objects.all()
        serializer = MilkingsystemSerializer(milkingsystems, many=True)
        return Response(serializer.data)


class EquipmentsView(APIView):
    # TODO add decorators
    def post(self, request, *args, **kwargs):
        data = request.data
        user = None if request.user.is_anonymous else request.user.id
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        organization = get_object_or_404(Organization, id=organizationid)
        data['organization'] = organization.id
        data['created_by'] = user
        data['modified_by'] = user
        serializer = EquipmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        equipments = Equipment.objects.all()
        serializer = EquipmentSerializer(equipments, many=True)
        return Response(serializer.data)


class LaboratoriesView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LaboratorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        gender = Laboratory.objects.all()
        serializer = LaboratorySerializer(gender, many=True)
        return Response(serializer.data)


class LaboratoryView(APIView):

    def get(self, request, *args, **kwargs):
        laboratory = get_object_or_404(Laboratory, id=kwargs['id'])
        serializer = LaboratorySerializer(laboratory)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        laboratory = get_object_or_404(Laboratory, id=kwargs['id'])
        serializer = LaboratorySerializer(laboratory, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)