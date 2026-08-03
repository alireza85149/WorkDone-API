from rest_framework import serializers
from apps.contracts.models import Contract

class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = (
            "id",
            "project",
            "proposal",
            "employer",
            "freelancer",
            "agreed_budget",
            "deadline",
            "status",
            "created_at",
        )
        read_only_fields = (
            'id',
            'project',
            'proposal',
            'employer',
            'freelancer',
            'agreed_budget',
            'deadline',
            'status',
            'created_at',
        )