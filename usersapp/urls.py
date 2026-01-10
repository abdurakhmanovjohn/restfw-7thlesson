from django.urls import path
from .views import SignUpView, VerifyCodeView, NewVerifyCodeView, UserChangeView

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('code-verify', VerifyCodeView.as_view()),
    path('new-verify-code', NewVerifyCodeView.as_view()),
    path('user-change-info', UserChangeView.as_view())
]