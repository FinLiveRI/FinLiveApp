from django.contrib.auth import get_user_model
from django.core.validators import EMPTY_VALUES
from rest_framework import serializers

from finliveapp.models import UserAccount, Organization, Barn, MilkingSystem, Equipment, SeedingType, Laboratory, \
    AccountOrganization


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
        fields = ('user', 'retries', 'usertype', 'created', 'modified', 'created_by', 'modified_by')
        read_only_fields = ('created', 'modified')

    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop('editor', None)
        self.organization = kwargs.pop('organization', None)
        super(UserAccountSerializer, self).__init__(*args, **kwargs)

    def validate(self, attrs):
        data = serializers.ModelSerializer.validate(self, attrs)
        validation_errors = {}
        if self.organization not in EMPTY_VALUES:
            if not self.editor.is_superuser:
                if not AccountOrganization.objects.filter(organization=self.organization,
                                                          account=self.editor.useraccount).exists():
                    validation_errors['organizations'] = "Not valid organization"
            else:
                if not AccountOrganization.objects.filter(organization=self.organization).exists():
                    validation_errors['organizations'] = "Not valid organization"
        else:
            validation_errors['organizations'] = "Not valid organization"
        if validation_errors not in EMPTY_VALUES:
            raise serializers.ValidationError(validation_errors)

        return data

    def create(self, validated_data):
        accountdata = validated_data
        accountdata['created_by'] = self.editor
        accountdata['modified_by'] = self.editor
        userdata = accountdata.pop('user')
        user = get_user_model().objects.create_user(**userdata)
        account = UserAccount.objects.create(user=user, **accountdata)
        if self.organization not in EMPTY_VALUES:
            AccountOrganization.objects.create(account=account, organization=self.organization)
        return account

    def update(self, instance, validated_data):
        if 'user' in validated_data:
            nested_serializer = self.fields['user']
            nested_instance = instance.user
            nested_data = validated_data.pop('user')
            nested_serializer.update(nested_instance, nested_data)

        data = validated_data
        data['modified_by'] = self.editor
        return super(UserAccountSerializer, self).update(instance, data)


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
    #organization = OrganizationSerializer()
    #created_by = UserAccountSerializer()
    #modified_by = UserAccountSerializer()

    class Meta:
        model = Barn
        fields = '__all__'
        read_only_fields = ('id', 'created', 'modified')

    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop('editor', None)
        super(BarnSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        data = validated_data
        data['created_by'] = self.editor
        data['modified_by'] = self.editor
        return data

    def update(self, instance, validated_data):
        data = validated_data
        data['modified_by'] = self.editor
        return super(BarnSerializer, self).update(instance, data)


class EquipmentSerializer(serializers.ModelSerializer):
    # organization = OrganizationSerializer(read_only=True)
    # created_by = UserSerializer(read_only=True)
    # modified_by = UserSerializer(read_only=True)

    class Meta:
        model = Equipment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'modified')

    def __init__(self, *args, **kwargs):
        #self.editor = kwargs.pop('editor', None)
        #self.organization = kwargs.pop('organization', None)
        super(EquipmentSerializer, self).__init__(*args, **kwargs)

    def validate(self, attrs):
        data = serializers.ModelSerializer.validate(self, attrs)
        return data

    # def create(self, validated_data):
    #     data = validated_data
    #     data['created_by'] = self.editor
    #     data['modified_by'] = self.editor
    #     data['organization'] = self.organization
    #     return super(EquipmentSerializer, self).create(data)

    def update(self, instance, validated_data):
        data = validated_data
        data['modified_by'] = self.editor
        return super(EquipmentSerializer, self).update(instance, data)


class MilkingsystemSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer()
    barn = BarnSerializer()
    organization = OrganizationSerializer()
    created_by = UserAccountSerializer()
    modified_by = UserAccountSerializer()

    class Meta:
        model = MilkingSystem
        fields = '__all__'
        read_only_fields = ('id', 'created', 'modified')

    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop('editor', None)
        super(MilkingsystemSerializer, self).__init__(*args, **kwargs)


class MilkingsystemViewSerializer(serializers.ModelSerializer):
    equipment = serializers.SlugRelatedField(slug_field='equipment.name', read_only=True)
    barn = serializers.SlugRelatedField(slug_field='barn.name', read_only=True)
    organization = serializers.SlugRelatedField(slug_field='organization.name', read_only=True)

    class Meta:
        model = MilkingSystem
        fields = '__all__'
        read_only_fields = ('id', 'created', 'modified')


class SeedingtypeSerializer(serializers.ModelSerializer):
    created_by = UserAccountSerializer(read_only=True)
    modified_by = UserAccountSerializer(read_only=True)

    class Meta:
        model = SeedingType
        fields = ('id', 'name', 'description', 'created', 'created_by', 'modified', 'modified_by')
        read_only_fields = ('id', 'created', 'modified')

    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop('editor', None)
        super(SeedingtypeSerializer, self).__init__(*args, **kwargs)


class LaboratorySerializer(serializers.ModelSerializer):
    created_by = UserAccountSerializer(read_only=True)
    modified_by = UserAccountSerializer(read_only=True)

    class Meta:
        model = Laboratory
        fields = ('id', 'name', 'description', 'created', 'created_by', 'modified', 'modified_by')
        read_only_fields = ('id', 'created', 'modified')

    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop('editor', None)
        super(LaboratorySerializer, self).__init__(*args, **kwargs)