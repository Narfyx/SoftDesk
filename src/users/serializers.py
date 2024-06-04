from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
            "birth_date",
            "can_be_contacted",
            "can_data_be_shared",
        )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            birth_date=validated_data["birth_date"],
            email=validated_data["email"],
            can_be_contacted=validated_data["can_be_contacted"],
            can_data_be_shared=validated_data["can_data_be_shared"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
            validated_data.pop("password")
        return super().update(instance, validated_data)
