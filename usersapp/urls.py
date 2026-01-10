from django.urls import path
from .views import SignUpView, VerifyCodeView

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('code-verify', VerifyCodeView.as_view())
]