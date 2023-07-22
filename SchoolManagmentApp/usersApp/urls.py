from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    # Home and Login&Logout
    path('', views.HomeView.as_view(), name="home"),
    path('account/logout/', views.LogoutView.as_view(template_name='index.html'), name='logout'),


    #Reset password
    path('account/reset_password/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('account/reset_password/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('account/reset_password/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),    
    path('account/reset_password/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
