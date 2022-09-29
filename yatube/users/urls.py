from django.contrib.auth.views import (LogoutView,
                                       LoginView,
                                       PasswordChangeView,
                                       PasswordChangeDoneView,
                                       PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView,
                                       )
from django.urls import path

from . import views


app_name = 'users'

pas_change = 'users/password_change_form.html'
pas_change_done = 'users/password_change_done.html'
pas_reset = 'users/password_reset_form.html'
pas_reset_done = 'users/password_reset_done.html'
pas_reset_confirm = 'users/password_reset_confirm.html'
pas_reset_complete = 'users/password_reset_complete.html'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('logout/',
         LogoutView.as_view(template_name='users/logged_out.html'),
         name='logout'
         ),
    path('login/',
         LoginView.as_view(template_name='users/login.html'),
         name='login'
         ),
    path('password_change/',
         PasswordChangeView.as_view(template_name=pas_change),
         name='password_change'
         ),
    path('password_change/done/',
         PasswordChangeDoneView.as_view(template_name=pas_change_done),
         name='password_change_done'
         ),
    path('password_reset/',
         PasswordResetView.as_view(template_name=pas_reset),
         name='password_reset'
         ),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name=pas_reset_done),
         name='password_reset_done'
         ),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name=pas_reset_confirm),
         name='password_reset_confirm'
         ),
    path('reset/done/',
         PasswordResetCompleteView.as_view(template_name=pas_reset_complete),
         name='password_reset_complete'
         ),
]
