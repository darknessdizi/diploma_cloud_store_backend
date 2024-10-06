from rest_framework import serializers
from .models import Users, Files


class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'