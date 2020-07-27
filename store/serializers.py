from rest_framework import serializers
from store.models import Box

class AdminBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['id','length','width','height','area','volume','created_by','created_on','updated_on']

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['id','length','width','height','area','volume','updated_on']