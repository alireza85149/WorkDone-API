from rest_framework import serializers
from apps.accounts.models import (User, FreelancerProfile, EmployerProfile)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "phone_number",
            "role",
        )
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )

        return value
    
    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        if user.role == User.Role.FREELANCER:
            FreelancerProfile.objects.create(
                user=user,
                first_name="",
                last_name=""
            )

        elif user.role == User.Role.EMPLOYER:
            EmployerProfile.objects.create(
                user=user,
                company_name=""
            )

        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone_number",
            "role",
            "is_verified",
        )