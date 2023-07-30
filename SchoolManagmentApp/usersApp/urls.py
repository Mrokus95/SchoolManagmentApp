from django.contrib import admin
from django.urls import path
from . import views 
from django.views.defaults import permission_denied

handler403 = permission_denied
urlpatterns = [
    # Home and Login&Logout
    path('home/', views.HomeView.as_view(), name="home"),
    path('account/logout/', views.LogoutView.as_view(template_name='index.html'), name='logout'),


    #Reset password
    path('reset_password/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('account/reset_password/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),    
    path('account/reset_password/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #Register new user
    path('account/register/student', views.StudentRegisterView.as_view(), name='register_student'),
    path('account/register/teacher', views.TeacherRegisterView.as_view(), name='register_teacher'),
    path('account/register/parent', views.ParentRegisterView.as_view(), name='register_parent'),
    path('account/register/complete/', views.RegistrationComplete.as_view(), name='registration_complete'),

    path('account/edit/', views.EditUserDataView.as_view(),name='update_user_profile'),

    #Changing password
    path('account/password_change/', views.CustomPaswordChangeView.as_view(), name = 'passwordChange'),
    path('account/password_change/done/', views.CustomPaswordChangeDoneView.as_view(), name = 'passwordChangeDone')]
