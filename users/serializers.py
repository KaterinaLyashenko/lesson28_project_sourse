from rest_framework import serializers
from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer

from users.models import User, Location


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class UserListSerializer(ModelSerializer):
    total_ads = IntegerField()
    class Meta:
        model = User
        fields = ['id', 'username', 'total_ads']

class UserCreateUpdateSerializer(ModelSerializer):
    locations = serializers.SlugRelatedField(many=True,
        read_only=True,
        slug_field='name',
        required=False)

    def is_valid(self, *, raise_exception=False):
        self.locations = self.initial_data.pop("location")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        new_user = User.objects.create(**validated_data)
        for loc_name in self.locations:
            loc, _ = Location.objects.get_or_crate(name=loc_name)
            new_user.locations.add(loc)

        return new_user

    def update(self, instance, validated_data):
        if self.locations:
            instance.locations.clear()
            for loc_name in self.locations:
                loc, _ = Location.objects.get_or_crate(name=loc_name)
                instance.locations.add(loc)
        return instance


    class Meta:
        model = User
        fields = '__all__'

class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'