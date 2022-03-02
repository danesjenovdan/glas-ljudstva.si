from rest_framework import serializers
from .models import Party

class PartySerializer(serializers.ModelSerializer):
    image_url = serializers.URLField()
    class Meta:
        model = Party
        fields = ['id', 'party_name', 'image_url', 'url']