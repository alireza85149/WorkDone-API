from rest_framework import serializers
from apps.reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)
    reviewer_id = serializers.IntegerField(source="reviewer.id", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "contract",
            "reviewer",
            "reviewer_id",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "reviewer", "reviewer_id", "created_at", "updated_at"]

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be an integer between 1 and 5.")
        return value
