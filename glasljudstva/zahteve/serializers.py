from rest_framework import serializers
from .models import Party

class PartySerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='user.id')
    image_url = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Party
        fields = ['id', 'party_name', 'image_url', 'url']
    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        else:
            return ''
