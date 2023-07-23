from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetView
from django.contrib.auth.models import User
from django.views.generic import FormView
from .forms import MyRegistrationForm
from .models import Profile, ClassUnit, Student

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


class RegistrationComplete(View):
    template_name = 'registration_complete.html'

    def get(self, request):
        return render(request, self.template_name)

class MyRegisterView(FormView):
    template_name = 'registration.html'
    form_class = MyRegistrationForm
    success_url = reverse_lazy('registration_complete')

    def form_valid(self, form):
        print(form.cleaned_data)
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        phone_number = form.cleaned_data['phone_number']
        account_type = form.cleaned_data['account_type']
        class_id = form.cleaned_data['class_id']
        photo= form.cleaned_data['photo']

        emailIsTaken = User.objects.filter(email=email).exists()
        usernameIsTaken = User.objects.filter(username=username).exists()

        if emailIsTaken and usernameIsTaken:
            form.add_error(None, 'Email and username already taken')
            return self.form_invalid(form)
        elif emailIsTaken:
            form.add_error('email', 'Email already taken')
            return self.form_invalid(form)
        elif usernameIsTaken:
            form.add_error('username', 'Username already taken')
            return self.form_invalid(form)

        # Tworzenie użytkownika
        user = User.objects.create_user(username=username, first_name = first_name, last_name=last_name, email=email, password=password1)

        # Dodanie profilu użytkownika
        profile = Profile.objects.create(user=user, phone_number=phone_number, photo=photo, account_type=account_type)

        # Tworzenie użytkowanika typu Student
        # class_unit = ClassUnit.objects.get(id=class_id)
        student = Student.objects.create(user=profile, klasa=class_id) 

        return super().form_valid(form)

    def form_invalid(self, form):
        # Obsługa błędów walidacji formularza
        return self.render_to_response(self.get_context_data(form=form))
    
    
