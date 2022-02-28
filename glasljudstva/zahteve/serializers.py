from rest_framework import serializers
from .models import Party

class PartySerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='user.id')
    class Meta:
        model = Party
        fields = ['id', 'party_name', 'image', 'url']
