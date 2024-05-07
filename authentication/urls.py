from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('phone_login', views.phone_login_view, name='phone_login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'), 
    path('confirm_admin/',views.confirm_admin, name='confirm_admin'),
    path('admin_cancel/',views.admin_cancel, name='admin_cancel'),
    
    # path('home/', views.home_page, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('change_pin/', views.change_pin, name='change_pin'),
    path('colaborator/',views.colaborator_list, name='colaborator'),
    # path('payment_home/', views.payment_view, name='payment_home'),

    path('clinic/', views.clinic_page, name='clinic'),

    # password change
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('get-states/', views.get_states, name='get_states'),
    path('get-districts/', views.get_districts, name='get_districts'),
    path('get-districts/<int:state_id>/', views.get_districts, name='get_districts_by_state'),

    #Forget Password Change
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
]