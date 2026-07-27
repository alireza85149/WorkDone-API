from rest_framework import serializers
from apps.submissions.models import Submission

class Submission(serializers.Serializer):
    model = Submission
    fields = '__all__'
    read_only_fields = [
        'id',
        'contract',
        'status',
        'submitted_at',
    ]