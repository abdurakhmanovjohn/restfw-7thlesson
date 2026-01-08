from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import VIA_EMAIL, VIA_PHONE, User


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    auth_type = serializers.UUIDField(read_only=True, required=False)
    auth_stat = serializers.UUIDField(read_only=True, required=False)

    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields["email_or_phone_number"] = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["id", "auth_type", "auth_stat"]
