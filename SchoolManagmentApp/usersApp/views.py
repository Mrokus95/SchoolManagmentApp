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
from .forms import RegistrationForm, TeacherRegistrationForm, ParentRegistrationForm
from .models import Profile, ClassUnit, Student, Parent
from eventApp.models import Teacher
from django.db import transaction

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

class StudentRegisterView(FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('registration_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = 'register_student'
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        password1 = form.cleaned_data['password1']
        phone_number = form.cleaned_data['phone_number']
        photo = form.cleaned_data['photo']

        with transaction.atomic():
            # Create a new user account
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password1)

            # Create a new profile
            profile = Profile.objects.create(user=user, phone_number=phone_number, photo=photo, account_type='Student')

            # Create a new student account
            student = Student.objects.create(user=profile)

        return super().form_valid(form)

    def form_invalid(self, form):
        for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(self.request, error)
        return self.render_to_response(self.get_context_data(form=form))
    
    
class TeacherRegisterView(FormView):
    template_name = 'registration.html'
    success_url = reverse_lazy('registration_complete')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registration_form'] = RegistrationForm()
        context['teacher_registration_form'] = TeacherRegistrationForm()
        context['view_name'] = 'register_teacher'
        return context
    

    def form_valid(self, form):

        registration_form = RegistrationForm(self.request.POST, self.request.FILES)
        teacher_registration_form = TeacherRegistrationForm(self.request.POST, self.request.FILES)

        if  registration_form.is_valid() and teacher_registration_form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            phone_number = form.cleaned_data['phone_number']
            photo = form.cleaned_data['photo']
            subject = form.cleaned_data['name']

        
            with transaction.atomic():
                # Create a new user account
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password1)

                # Create a new profile
                profile = Profile.objects.create(user=user, phone_number=phone_number, photo=photo, account_type='Teacher')

                # Create a new teacher account
                teacher = Teacher.objects.create(user=profile, lesson_type=subject)

            return super().form_valid(form)
        else:

            return self.render_to_response(self.get_context_data(form=registration_form, teacher_registration_form=teacher_registration_form ))


    def form_invalid(self, form):
        registration_form = RegistrationForm(self.request.POST, self.request.FILES)
        teacher_registration_form = TeacherRegistrationForm(self.request.POST, self.request.FILES)

        for field_errors in form.errors.values():
            for error in field_errors:
                messages.error(self.request, error)

        return self.render_to_response(self.get_context_data(registration_form=registration_form, teacher_registration_form=teacher_registration_form))
    

class ParentRegisterView(FormView):
    template_name = 'registration.html'
    success_url = reverse_lazy('registration_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registration_form'] = RegistrationForm()
        context['parent_registration_form'] = ParentRegistrationForm()
        context['view_name'] = 'register_parent'
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return ParentRegistrationForm(self.request.POST, self.request.FILES)

    def form_valid(self, form):
        registration_form = RegistrationForm(self.request.POST, self.request.FILES)
        parent_registration_form = ParentRegistrationForm(self.request.POST, self.request.FILES)

        if registration_form.is_valid() and parent_registration_form.is_valid():
            username = registration_form.cleaned_data['username']
            first_name = registration_form.cleaned_data['first_name']
            last_name = registration_form.cleaned_data['last_name']
            email = registration_form.cleaned_data['email']
            password1 = registration_form.cleaned_data['password1']
            phone_number = registration_form.cleaned_data['phone_number']
            photo = registration_form.cleaned_data['photo']
            student = parent_registration_form.cleaned_data['student']

            with transaction.atomic():
                # Create a new user account
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password1)

                # Create a new profile
                profile = Profile.objects.create(user=user, phone_number=phone_number, photo=photo, account_type='Parent')

                # Create a new parent account
                parent = Parent.objects.create(user=profile, student=student)
            print("Form is valid1!")
            return super().form_valid(form)
        else:
            
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(self.request, error)
             # Print individual field errors
            for field in registration_form:
                if field.errors:
                    print(f"Field '{field.name}': {field.errors} {field.data}")
            for field in parent_registration_form:
                if field.errors:
                    print(f"Field parent '{field.name}': {field.errors}")

            return self.render_to_response(self.get_context_data(registration_form=registration_form, parent_registration_form=parent_registration_form))

    def form_invalid(self, form):
        registration_form = RegistrationForm(self.request.POST, self.request.FILES)
        parent_registration_form = ParentRegistrationForm(self.request.POST, self.request.FILES)

        for field_errors in form.errors.values():
            for error in field_errors:
                messages.error(self.request, error)
        print("Form is invalid2!")
        return self.render_to_response(self.get_context_data(registration_form=registration_form, parent_registration_form=parent_registration_form))