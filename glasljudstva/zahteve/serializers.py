from rest_framework import serializers

from .models import Demand, DemandAnswer, Municipality, Party, WorkGroup


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


class PartyVolitvomatSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="party_name")

    class Meta:
        model = Party
        fields = ["id", "name", "image"]


class WorkGroupVolitvomatSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkGroup
        fields = ["id", "name"]


class DemandVolitvomatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demand
        fields = ["id", "title", "list_title", "description", "workgroup_id"]


class DemandAnswerVolitvomatSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField(source="demand_id")
    agreement = serializers.BooleanField(source="agree_with_demand")

    class Meta:
        model = DemandAnswer
        fields = ["id", "question_id", "party_id", "comment", "agreement"]
