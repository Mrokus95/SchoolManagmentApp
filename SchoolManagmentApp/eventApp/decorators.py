from django.contrib import messages
from django.shortcuts import redirect

def student_required(func):
    def _wrapped_func(request, *args, **kwargs):
        profile=request.user.profile.account_type
        if profile != 'Student':
            messages.error(request, "Only for Students!")
            return redirect('home')         
        return func(request, *args, **kwargs)  
    return _wrapped_func

def parent_required(func):
    def _wrapped_func(request, *args, **kwargs):
        profile=request.user.profile.account_type
        if profile  != 'Parent':
            messages.error(request, "Only for Parents!")
            return redirect('home')         
        return func(request, *args, **kwargs)  
    return _wrapped_func