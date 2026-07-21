from rest_framework import serializers
from proposals.models import Proposal

class ProposalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proposal
        fields = "__all__"
        read_only_fields = (
            "id",
            "project",
            "freelancer",
            "status",
            "created_at",
        )