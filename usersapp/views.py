from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from .serializers import SignUpSerializer
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