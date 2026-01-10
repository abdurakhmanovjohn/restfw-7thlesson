from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework import permissions
from .serializers import SignUpSerializer, UserChangeInfoSerializer
from .models import *
from rest_framework.validators import ValidationError
from rest_framework.response import Response
from datetime import datetime

class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny, )


class VerifyCodeView(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')

        self.check_verify_code(user, code)
        data = {
            "success": True,
            "auth_status": user.auth_status,
            "access_token": user.token()['access'],
            "refresh": user.token()['refresh']
        }

        return Response(data)
    
    @staticmethod
    def check_verify_code(user, code):
        verify = user.verify_codes.filter(code=code, confirmed=False, expiration_time__gte=datetime.now())

        if not verify.exists():
            data = {
                "success": False,
                "message": "Code is expired or wrong"
            }
            raise ValidationError(data)
        
        else:
            # verify.confirmed = True
            verify.update(confirmed=True)

        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()
        
        return True


class NewVerifyCodeView(CreateAPIView):
    permission_classes = (permissions.IsAuthenticated)

    def get(self, request):
        user = request.user
        self.check_code(user)

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
        
        data = {
            'success': True,
            'message': 'Code sent!'
        }
        
        return Response(data)
    
    @staticmethod
    def check_code(user):
        verify = user.verify_codes.filter(confirmed=False, expiration_time__gte=datetime.now())

        if verify.exists():
            data = {
                "success": False,
                "message": "you have an active code"
            }
            raise ValidationError(data)

        if user.auth_status != NEW:
            data = {
                'success': False,
                'message': 'code already confirmed'
            }
            raise ValidationError(data)
        
        return True


class UserChangeView(UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated)
    queryset = User.objects.all()
    serializer_class = UserChangeInfoSerializer

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        data = {
            'success': True,
            'message': "info updated"
        }

        return Response(data)
    
    def partial_update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        data = {
            'success': True,
            'message': "info updated partially"
        }

        return Response(data)