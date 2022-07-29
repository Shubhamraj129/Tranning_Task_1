from rest_framework import serializers
from .models import Create_User
from django.contrib.auth.hashers import make_password


class User_Serializer(serializers.ModelSerializer):
    @staticmethod
    def validate_password(password: str) -> str:
        return make_password(password)

    class Meta:
        model = Create_User
        fields = [
            'id', 'username', 'password', 'date_of_birth', 'phone_number',
            'street', 'zip_code', 'email', 'city', 'state', 'country', 'first_name', 'last_name'
        ]


class User_Update_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Create_User
        fields = [
            'id', 'date_of_birth', 'phone_number',
            'street', 'zip_code', 'city', 'state', 'country', 'first_name', 'last_name'
        ]


class Change_Password(serializers.Serializer):
    model = Create_User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class Forget_password(serializers.ModelSerializer):
    """
        This serializer is used to send email forget password link
    """
    email = serializers.EmailField()

    class Meta:
        model = Create_User
        fields = [
            'email'
        ]


class New_Password(serializers.ModelSerializer):
    """
        This serializer is used to put new Password
    """
    class Meta:
        model = Create_User
        fields = [
            'password'
        ]
