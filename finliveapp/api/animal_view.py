from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from finliveapp.common.utils import dictTolist
from finliveapp.models import Animal, Organization, Barn, Breed, Gender
from finliveapp.serializers.animal_serializers import AnimalSerializer, BreedSerializer, GenderSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class Animals(APIView):

    # TODO add decorators
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        result = []
        animallist = dictTolist(data)
        if not animallist:
            return Response({'error': "Animal data missing"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                for animal in animallist:
                    organization = get_object_or_404(Organization, name=animal.get('organization').lower())
                    barn = get_object_or_404(Barn, farmid=animal.get('farmid'))
                    breed = get_object_or_404(Breed, abbreviation=animal.get('breed'))
                    animal['oranization'] = organization
                    animal['breed'] = breed
                    animal['barn'] = barn
                    serializer = AnimalSerializer(data=animal)
                    if serializer.is_valid():
                        serializer.save()
                        result.append(serializer.data)
            return Response(result, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'Animal creation failed'}, status=status.HTTP_400_BAD_REQUEST)


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


class GenderView(APIView):

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
            return Response({'error': 'Breed creation failed'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        gender = Gender.objects.all()
        serializer = GenderSerializer(gender, many=True)
        return Response(serializer.data)
