from rest_framework import serializers

from autoticketsys.models import ParkingDetails, SlotDetails

class ParkingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingDetails
        fields = '__all__'

class SlotDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SlotDetails
        fields = '__all__'