from django.urls import path
from account.views.account import PasswordChangeView, UpdateTwoFactorAuthenticationView, UserProfileView
from account.views.auth import PasswordResetConfirmView, PasswordResetRequestView

urlpatterns = [

    path('', UserProfileView.as_view()),
    path('password/change/', PasswordChangeView.as_view(), name='password-change'),
    path('password/reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('two-factor', UpdateTwoFactorAuthenticationView.as_view(), name='UpdateTwoFactorAuthenticationView'),
]
