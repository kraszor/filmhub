from django.urls import path, re_path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views


urlpatterns = [
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register'),
    path('profile', views.profile, name='profile'),
    path('edit_profile', views.edit_profile, name='edit'),
    path('change_password', views.change_password, name='change_password'),
    path('reset_password', PasswordResetView.as_view(), name='reset_password'),
    path('reset_password/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),



]
