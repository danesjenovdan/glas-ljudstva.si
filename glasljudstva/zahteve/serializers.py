from rest_framework import serializers
from .models import Party

class PartySerializer(serializers.ModelSerializer):
    image_url = serializers.URLField()
    municipality = serializers.StringRelatedField()

    class Meta:
        model = Party
        fields = ['id', 'party_name', 'image_url', 'url', 'proposer', 'sex', 'is_winner', 'municipality']