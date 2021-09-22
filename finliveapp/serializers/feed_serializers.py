from datetime import datetime
from django.core.validators import EMPTY_VALUES

from finliveapp.models import Feed, FeedAnalysis, Feeding

from rest_framework import serializers

from finliveapp.serializers.management_serializer import OrganizationSerializer, UserAccountSerializer


class FeedSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()
    created_by = UserAccountSerializer()
    modified_by = UserAccountSerializer()

    class Meta:
        model = Feed
        fields = '__all__'
        read_only_fields = ('id', 'created', 'modified')


