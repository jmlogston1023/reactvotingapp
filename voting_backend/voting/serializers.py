from rest_framework import serializers
from .models import VoteRecord

class VoterActivitySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email")
    ballot = serializers.CharField(source="ballot.title")

    class Meta:
        model = VoteRecord
        fields = ["email", "ballot", "voted_at"]
