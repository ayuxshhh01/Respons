from rest_framework import serializers
from .models import *



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'phone_number', 'emergency_contact']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    

class LocationSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()






class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'user', 'alert_type', 'location', 'timestamp']
        read_only_fields = ['user', 'location']



class DashboardUserSerializer(serializers.ModelSerializer):
    # We will add the last_location field to the model later.
    # For now, this is a placeholder.
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'is_staff'] # Add last_location later