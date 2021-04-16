from rest_framework import serializers
from .models import Frequency, ServiceArea, CleaningType, BasePrice, Room, Bathroom, ExtraOption


class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceArea
        fields = ['description', 'price', 'minutes']


class CleaningTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CleaningType
        fields = ['description', 'price', 'minutes']


class BasePriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasePrice
        fields = ['description', 'price']


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['description', 'price', 'minutes']


class BathroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bathroom
        fields = ['description', 'price', 'minutes']


class ExtraOptsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExtraOption
        fields = ['description', 'price', 'minutes']

