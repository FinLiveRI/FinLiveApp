from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404

from finliveapp.common.utils import dictTolist
from finliveapp.models import Animal, Barn, Feed, FeedAnalysis, Organization
from finliveapp.serializers.feed_serializers import FeedSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class FeedsView(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user.useraccount
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
                        feed['organization'] = get_object_or_404(Organization, id=feed.get('organization'))
                    feed['modified_by'] = user
                    feed['created_by'] = user
                    feedserializer = FeedSerializer(data=feed)
                    if feedserializer.is_valid():
                        newfeed = feedserializer.save()
                        result.append(newfeed.data)
            return Response(result, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'Animal creation failed'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        # organizationid = self.request.META.get('HTTP_X_ORG', None)
        feeds = Feed.objects.all()
        serializer = FeedSerializer(feeds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FeedView(APIView):

    def get(self, request, *args, **kwargs):
        feed = get_object_or_404(Feed, id=kwargs['id'])
        serializer = FeedSerializer(feed)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        feed = get_object_or_404(Animal, id=kwargs['id'])
        serializer = FeedSerializer(feed, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)