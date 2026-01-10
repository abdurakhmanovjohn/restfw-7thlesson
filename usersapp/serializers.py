from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import VIA_EMAIL, VIA_PHONE, User

from sharedapp.utility import email_or_phone_number 


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    auth_type = serializers.UUIDField(read_only=True, required=False)
    auth_stat = serializers.UUIDField(read_only=True, required=False)

    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields["email_or_phone_number"] = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["id", "auth_type", "auth_stat"]
    
    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)

        if user.auth_type == VIA_EMAIL:
            code = user.generate_code(VIA_EMAIL)
            # code = user.verify_code(VIA_EMAIL)
            # send_mail(user.email, code)
            print(code)
        elif user.auth_type == VIA_PHONE:
            code = user.generate_code(VIA_PHONE)
            # code = user.verify_code(VIA_PHONE)
            # send_phone_number_sms(user.phone_number, code)
            print(code)
        
        user.save()
        return user

    
    def validate(self, data):
        super(SignUpSerializer, self).validate(data)
        data = self.auth_validate(data)
        return data

    @staticmethod
    def auth_validate(data):
        user_input = str(data.get('email_or_phone_number'))
        user_input_type = email_or_phone_number(user_input)

        # print(f"user_input: {user_input} \nuser_input_type: {user_input_type}")

        if user_input_type == 'email':
            data = {
                'email': user_input,
                'auth_type': VIA_EMAIL
            }
        elif user_input_type == 'phone':
            data = {
                'phone_number': user_input,
                'auth_type': VIA_PHONE
            }
        else:
            data = {
                'success': 'False',
                'message': 'pls input phone number or email'
            }

            raise ValidationError(data)
        
        return data

    def validate_email_or_phone_number(self, value:str):
        value = value.lower()

        if value and User.objects.filter(email=value).exists():
            raise ValidationError('This email already has been registered')

        elif value and User.objects.filter(phone_number=value).exists():
            raise ValidationError('This phone number already has been registered')

        
        return value
    
    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.token())
        return data