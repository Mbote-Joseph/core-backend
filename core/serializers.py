from rest_framework import serializers
from .models import SuperAdmin, Admin, Visitor, Building, Floor, Room

class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperAdmin
        fields = ['full_name', 'email', 'id_number', 'phone_number', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        superadmin = SuperAdmin(**validated_data)
        superadmin.set_password(password)
        superadmin.save()
        return superadmin

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['full_name', 'email', 'id_number', 'building', 'phone_number', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        admin = Admin(**validated_data)
        admin.set_password(password)
        admin.save()
        return admin

class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = ['full_name', 'id_number', 'phone_number']

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['name', 'superadmin']

class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['building', 'floor_number']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['floor', 'room_number', 'is_office']
