from django.contrib.auth import get_user_model
from rest_framework import serializers

from finliveapp.models import UserAccount, Organization, Barn


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'password', 'username', 'first_name', 'last_name',
                  'email', 'is_active', 'last_login', 'date_joined')
        read_only_fields = ('id', 'last_login', 'date_joined')
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }


class UserAccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserAccount
        fields = ('id', 'user', 'retries', 'usertype', 'created', 'modified')
        read_only_fields = ('id', 'created', 'modified')

    def create(self, validated_data):
        accountdata = validated_data
        userdata = accountdata.pop('user')
        user = get_user_model().objects.create_user(**userdata)
        account = UserAccount.objects.create(user=user, **accountdata)
        return account


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = '__all__'
        read_only_fields = ('id', 'apikey', 'created', 'modified')

    def validate(self, attrs):
        data = serializers.ModelSerializer.validate(self, attrs)
        name = data.get('name', '').lower()
        if not self.instance or self.instance.name != name:
            exists = Organization.objects.filter(name=name).exists()
            if exists:
                raise serializers.ValidationError({'name': "Given name is already in use"})
        return data

    def to_internal_value(self, data):
        data = super(OrganizationSerializer, self).to_internal_value(data)
        data['name'] = data.get('name').lower()
        return data


class BarnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barn
        fields = '__all__'
        read_only_fields = ('id', 'created', 'modified')
