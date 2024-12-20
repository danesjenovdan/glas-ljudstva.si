from rest_framework import serializers

from .models import Municipality, Party


class PartySerializer(serializers.ModelSerializer):
    image_url = serializers.URLField()

    class Meta:
        model = Party
        fields = [
            "id",
            "party_name",
            "image_url",
            "url",
            "proposer",
            "sex",
            "is_winner",
            "municipality",
            "already_has_pp",
        ]


class MunicipalitySerializer(serializers.ModelSerializer):
    image = serializers.URLField()

    class Meta:
        model = Municipality
        fields = ["id", "name", "email", "image", "slug"]
