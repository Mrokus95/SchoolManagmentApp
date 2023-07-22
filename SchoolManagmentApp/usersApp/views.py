from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render

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
        
    
