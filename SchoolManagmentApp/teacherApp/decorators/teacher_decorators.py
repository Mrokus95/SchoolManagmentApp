
def teacher_required(func):
    def _wrapped_func(request, *args, **kwargs):
        if request.user.profile.account_type != 'Teacher':
            messages.error(request, "Only for teachers!")
            return redirect('home')         
        return func(request, *args, **kwargs)  
    return _wrapped_func