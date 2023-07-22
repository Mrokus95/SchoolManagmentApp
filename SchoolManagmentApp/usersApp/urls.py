from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('logout/', views.LogoutView.as_view(template_name='index.html'), name='logout')
]
