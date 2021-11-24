from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404

from finliveapp.common.utils import dictTolist
from finliveapp.decorators.access import check_user_organization, check_user_or_apikey
from finliveapp.models import Animal, Barn, Feed, FeedAnalysis, Organization, Feeding
from finliveapp.serializers.feed_serializers import FeedSerializer, FeedingSerializer, NewFeedingSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class FeedsView(APIView):
    @check_user_or_apikey()
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        organization = get_object_or_404(Organization, id=organizationid)
        result = []
        feedlist = dictTolist(data)
        try:
            with transaction.atomic():
                for feed in feedlist:
                    if 'organization' not in feed:
                        feed['organization'] = organization
                    else:
                        feed['organization'] = get_object_or_404(Organization, id=feed.get('organization')).id
                    feed['modified_by'] = None if user.is_anonymous else user.id
                    feed['created_by'] = None if user.is_anonymous else user.id
                    feedserializer = FeedSerializer(data=feed)
                    if feedserializer.is_valid(raise_exception=True):
                        feedserializer.save()
                        result.append(feedserializer.data)
            return Response(result, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'Animal creation failed'}, status=status.HTTP_400_BAD_REQUEST)

    @check_user_or_apikey()
    def get(self, request, *args, **kwargs):
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        feeds = Feed.objects.filter(organization_id=organizationid)
        serializer = FeedSerializer(feeds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FeedView(APIView):
    @check_user_or_apikey()
    def get(self, request, *args, **kwargs):
        feed = get_object_or_404(Feed, id=kwargs['id'])
        serializer = FeedSerializer(feed)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @check_user_or_apikey()
    def patch(self, request, *args, **kwargs):
        feed = get_object_or_404(Feed, id=kwargs['id'])
        user = request.user
        data = request.data
        data['modified_by'] = None if user.is_anonymous else user.id
        serializer = FeedSerializer(feed, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedingView(APIView):
    @check_user_or_apikey()
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        if user.is_anonymous:
            user = None
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        feedinglist = dictTolist(data)
        serializer = NewFeedingSerializer(data=feedinglist, **{'editor': user, 'organization': organizationid}, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_user_or_apikey()
    def get(self, request, *args, **kwargs):
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        feeds = Feeding.objects.filter(organization_id=organizationid)
        serializer = FeedingSerializer(feeds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FeedingSingleView(APIView):
    @check_user_or_apikey()
    def get(self, request, *args, **kwargs):
        feeding = get_object_or_404(Feeding, id=kwargs['id'])
        serializer = FeedSerializer(feeding)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @check_user_or_apikey()
    def patch(self, request, *args, **kwargs):
        feeding = get_object_or_404(Feeding, id=kwargs['id'])
        organizationid = self.request.META.get('HTTP_X_ORG', None)
        user = request.user
        data = request.data
        serializer = FeedingSerializer(feeding, data=request.data, **{'editor': user, 'organization': organizationid}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
