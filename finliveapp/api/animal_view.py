from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from finliveapp.common.utils import dictTolist
from finliveapp.decorators.access import check_user_or_apikey
from finliveapp.models import Animal, Organization, Barn, Breed, Gender, SeedingType
from finliveapp.serializers.animal_serializers import AnimalSerializer, BreedSerializer, GenderSerializer, \
    NewAnimalSerializer, AnimalViewSerializer, SeedingtypeSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class Animals(APIView):

    @check_user_or_apikey()
    def post(self, request, *args, **kwargs):
        data = request.data
        user = None if request.user.is_anonymous else request.user
        result = []
        animallist = dictTolist(data)
        if not animallist:
            return Response({'error': "Animal data missing"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                for animal in animallist:
                    _organization = animal.get('organization')
                    if isinstance(_organization, int):
                        organization = get_object_or_404(Organization, id=animal.get('organization'))
                    else:
                        organization = get_object_or_404(Organization, name=animal.get('organization').lower())
                    barn = get_object_or_404(Barn, farmid=animal.get('farmid'))
                    breed = get_object_or_404(Breed, abbreviation=animal.get('breed'))
                    gender = get_object_or_404(Gender, abbreviation=animal.get('gender'))

                    serializer = NewAnimalSerializer(data=animal)
                    if serializer.is_valid():
                        serializer.validated_data['organization'] = organization
                        serializer.validated_data['barn'] = barn
                        serializer.validated_data['breed'] = breed
                        serializer.validated_data['gender'] = gender
                        serializer.validated_data['created_by'] = user
                        serializer.validated_data['modified_by'] = user
                        new_animal = Animal.objects.create(**serializer.validated_data)
                        result.append(new_animal)
                    else:
                        raise Exception(serializer.errors)
            serializer = AnimalViewSerializer(result, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'Animal creation failed'}, status=status.HTTP_400_BAD_REQUEST)

    @check_user_or_apikey()
    def get(self, request, *args, **kwargs):
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        organization = get_object_or_404(Organization, id=organizationid)
        animals = Animal.objects.filter(organization=organization)
        serializer = AnimalViewSerializer(animals, many=True)
        return Response(serializer.data)


class AnimalView(APIView):
    @check_user_or_apikey()
    def get(self, request, *args, **kwargs):
        animal = get_object_or_404(Animal, id=kwargs['id'])
        serializer = AnimalSerializer(animal)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @check_user_or_apikey()
    def patch(self, request, *args, **kwargs):
        animal = get_object_or_404(Animal, id=kwargs['id'])
        user = None if request.user.is_anonymous else request.user
        serializer = AnimalSerializer(animal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['modified_by'] = user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BreedsView(APIView):
    # TODO add decorators
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        breedlist = dictTolist(data)
        if not breedlist:
            return Response({'error': "Breed data missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = BreedSerializer(data=breedlist, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({'error': 'Breed creation failed'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        breeds = Breed.objects.all()
        serializer = BreedSerializer(breeds, many=True)
        return Response(serializer.data)


class BreedView(APIView):
    def get(self, request, *args, **kwargs):
        breed = get_object_or_404(Breed, id=kwargs['id'])
        serializer = BreedSerializer(breed)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        breed = get_object_or_404(Breed, id=kwargs['id'])
        serializer = BreedSerializer(breed, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GendersView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        genderlist = dictTolist(data)
        if not genderlist:
            return Response({'error': "Gender data missing"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer = GenderSerializer(data=genderlist, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({'error': 'Gender creation failed'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        gender = Gender.objects.all()
        serializer = GenderSerializer(gender, many=True)
        return Response(serializer.data)


class GenderView(APIView):
    def get(self, request, *args, **kwargs):
        gender = get_object_or_404(Gender, id=kwargs['id'])
        serializer = GenderSerializer(gender)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        gender = get_object_or_404(Gender, id=kwargs['id'])
        serializer = GenderSerializer(gender, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SeedingtypesView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GenderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        gender = SeedingType.objects.all()
        serializer = SeedingtypeSerializer(gender, many=True)
        return Response(serializer.data)


class SeedingtypeView(APIView):

    def get(self, request, *args, **kwargs):
        seedingtype = get_object_or_404(SeedingType, id=kwargs['id'])
        serializer = SeedingtypeSerializer(seedingtype)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        seedingtype = get_object_or_404(SeedingType, id=kwargs['id'])
        serializer = SeedingtypeSerializer(seedingtype, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)