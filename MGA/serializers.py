import re

from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField

from MGA.models import User, Event, Organization


class PUserSerializer(serializers.ModelSerializer):
    confirm_url = HyperlinkedIdentityField(
        view_name='MGA:confirm',
        lookup_field='id'
    )

    def validate_username(self, value):
        qs = User.objects.filter(username__exact=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("Username should be unique")
        return value

    def validate_phone_number(self, value):
        if len(value) != 11:
            raise serializers.ValidationError("Your phone number should have 11 digits")
        rule = re.compile(r'/^09[0-9]{9}$/')
        if not rule.search(value):
            raise serializers.ValidationError("Your phone number is incorrect")
        return value

    def validate_bio(self, value):
        if len(value) > 249:
            raise serializers.ValidationError("Your bio should have at least 250 characters")

    def validate_password(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Your password is too short! It must be between 5 and 15 characters")
        if len(value) > 15:
            raise serializers.ValidationError("Your password is too long! It must be between 5 and 15 characters")
        if not re.search(r'[A-Z]|[a-z]', value) & re.search("[!@#$%^&*]", value):
            raise serializers.ValidationError("Weak password!")
        if not re.search("[0-9]", value) & re.search("[!@#$%^&*]", value):
            raise serializers.ValidationError("Weak password!")
        return value

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'city', 'bio', 'phoneNumber', 'password','confirm_url']


class EventSerializer(serializers.ModelSerializer):
    members = PUserSerializer(read_only=True, many=True)  # todo am i doing this right?

    class Meta:
        model = Event
        fields = ['date', 'capacity', 'owner', 'members', 'title', 'description']


class OrganizationSerializer(serializers.ModelSerializer):
    admins = PUserSerializer(read_only=True, many=True)  # todo am i doing this right?

    class Meta:
        model = Organization
        fields = ['name', 'creator', 'admins']
