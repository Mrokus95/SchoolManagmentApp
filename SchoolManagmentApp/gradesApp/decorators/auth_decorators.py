from django.contrib import messages
from django.shortcuts import redirect


def teacher_and_staff_only(func):
    def _wrapped_func(request, *args, **kwargs):
        if request.user.profile.account_type not in ["Teacher", "Admin"]:
            messages.error(request, "Only for teachers and staff!")
            return redirect("home")
        return func(request, *args, **kwargs)

    return _wrapped_func
