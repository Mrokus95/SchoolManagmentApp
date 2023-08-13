from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.defaults import permission_denied
from . import views

handler403 = permission_denied
urlpatterns = [
    path(
        "home/", 
        views.HomeView.as_view(), 
        name="home",
        ),
    path("home/authors", 
        views.AuthorsView.as_view(), 
        name="authors",
        ),
    path(
        "account/logout/",
        LogoutView.as_view(template_name="index.html"),
        name="logout",
    ),
    path(
        "reset_password/",
        views.CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "reset_password/done/",
        views.CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "account/reset_password/confirm/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "account/reset_password/complete/",
        views.CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "account/register/student",
        views.StudentRegisterView.as_view(),
        name="register_student",
    ),
    path(
        "account/register/teacher",
        views.TeacherRegisterView.as_view(),
        name="register_teacher",
    ),
    path(
        "account/register/parent",
        views.ParentRegisterView.as_view(),
        name="register_parent",
    ),
    path(
        "account/register/complete/",
        views.RegistrationComplete.as_view(),
        name="registration_complete",
    ),
    path("account/edit/", 
         views.EditUserDataView.as_view(), 
         name="update_user_profile"),
    path(
        "account/password_change/",
        views.CustomPaswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "account/password_change/done/",
        views.CustomPaswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]
