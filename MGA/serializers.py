import re

from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField

from MGA.models import User, Event, Organization, Notification, Reason


class UserSerializer(serializers.ModelSerializer):
    confirm_url = HyperlinkedIdentityField(
        view_name='MGA:confirm',
        lookup_field='id'
    )
    password = serializers.CharField(
        max_length=128,
        min_length=4,
        write_only=True
    )

    def validate_username(self, value):
        qs = User.objects.filter(username__exact=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("Username should be unique")
        return value

    def validate_phoneNumber(self, value):
        if len(str(value)) != 10:
            raise serializers.ValidationError("Your phone number should have 10 digits")
        rule = re.compile("^9[0-9]{9}$")
        if not rule.search(str(value)):
            raise serializers.ValidationError("Your phone number is incorrect")
        return value

    def validate_bio(self, value):
        if len(str(value)) > 249:
            raise serializers.ValidationError("Your bio should have at least 250 characters")

    def validate_password(self, value):
        if len(str(value)) < 5:
            raise serializers.ValidationError("Your password is too short! It must be between 5 and 15 characters")
        if len(str(value)) > 15:
            raise serializers.ValidationError("Your password is too long! It must be between 5 and 15 characters")
        if not re.search(r'[A-Z]|[a-z]', value):
            if not re.search("[!@#$%^&*]", value):
                raise serializers.ValidationError("Weak password!")
        if not re.search("[0-9]", value):
            if not re.search("[!@#$%^&*]", value):
                raise serializers.ValidationError("Weak password!")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'city', 'bio', 'phoneNumber', 'password', 'confirm', 'confirm_url']


class EventSerializer(serializers.ModelSerializer):
    members = UserSerializer(read_only=True, many=True)

    confirm_url = HyperlinkedIdentityField(
        view_name=''

    )

    class Meta:
        model = Event
        fields = ['date', 'capacity', 'owner', 'members', 'title', 'description']  # todo add location


class OrganizationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name', 'creator', 'admins']


class OrganizationSerializer(serializers.ModelSerializer):
    admins = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Organization
        fields = ['name', 'creator', 'admins']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = '__all__'


