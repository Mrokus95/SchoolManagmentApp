from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetView
from django.urls import reverse_lazy

class HomeView(View):
    template_name = 'index.html'

    def get(self, request):
        form = AuthenticationForm()
        context = {'form': form, 'next': request.GET.get('next', '')}
        return render(request, self.template_name, context)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                redirect_to = request.POST.get('next', '')
                if redirect_to and self._is_safe_redirect(redirect_to):
                    return HttpResponseRedirect(redirect_to)
                return HttpResponseRedirect(reverse_lazy('home'))
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
            context = {'form': form, 'next': request.GET.get('next', '')}
            return render(request, self.template_name, context)
        

class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy("password_reset_done")
    template_name = "password_reset_form.html"
    html_email_template_name = "password_reset_email.html"

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "password_reset_done.html"

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
        success_url = reverse_lazy("password_reset_complete")
        template_name = "password_reset_confirm.html"

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['uidb64'] = self.kwargs['uidb64']
            context['token'] = self.kwargs['token']
            return context

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "password_reset_complete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
