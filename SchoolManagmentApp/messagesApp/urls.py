from django.contrib import admin
from django.urls import path
from . import views 
from django.views.defaults import permission_denied

handler403 = permission_denied
urlpatterns = [
    # Home and Login&Logout
    path('', views.get_inbox, name="inbox"),]
