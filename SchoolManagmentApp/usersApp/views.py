from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetView,PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.models import User
from django.views.generic import FormView
from .forms import RegistrationForm, TeacherRegistrationForm, StudentRegistrationForm, UserEditForm, ProfileEditForm
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Profile, Student, Parent
from eventApp.models import Teacher
from django.db import transaction
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied



def staff_check(user):
    return user.is_authenticated and user.is_staff

class AuthorsView(View):
    template_name = 'authors.html'
    
    def get(self, request):
        return render(request, self.template_name)

class HomeView(View):
    template_name = 'index.html'

    def get(self, request):

        
        if request.user.is_authenticated:
            return redirect('view_schedule')

        form = AuthenticationForm()
        next_url = request.GET.get('next', '')

        context = {'form': form, 'next': next_url}
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
                if redirect_to and url_has_allowed_host_and_scheme(redirect_to, allowed_hosts=None):
                    return redirect(redirect_to)
                return redirect('events')
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


class RegistrationComplete(UserPassesTestMixin, View):
    template_name = 'registration_complete.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def test_func(self):
        return staff_check(self.request.user)

    def handle_no_permission(self):
        raise PermissionDenied()

class ParentRegisterView(UserPassesTestMixin, FormView):
    template_name = 'registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('registration_complete')
    context_object_name = 'registration_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registration_form'] = context['form']
        context['view_name'] = 'register_parent'
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
            if photo:
                profile = Profile.objects.create(user=user, phone_number=phone_number, photo=photo, account_type='Parent')
            else:
                profile = Profile.objects.create(user=user, phone_number=phone_number, account_type='Parent')

            # Create a new student account
            parent = Parent.objects.create(user=profile)

        return super().form_valid(form)

    def form_invalid(self, form):
        for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(self.request, error)
        return self.render_to_response(self.get_context_data(form=form))
    
    def test_func(self):
        return staff_check(self.request.user)

    def handle_no_permission(self):
        raise PermissionDenied()
    
class TeacherRegisterView(UserPassesTestMixin, FormView):
    template_name = 'registration.html'
    success_url = reverse_lazy('registration_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registration_form'] = RegistrationForm()
        context['teacher_registration_form'] = TeacherRegistrationForm()
        context['view_name'] = 'register_teacher'
        return context
    
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return TeacherRegistrationForm(self.request.POST, self.request.FILES)

    def form_valid(self, form):
        registration_form = RegistrationForm(self.request.POST, self.request.FILES)
        teacher_registration_form = TeacherRegistrationForm(self.request.POST, self.request.FILES)

        if registration_form.is_valid() and teacher_registration_form.is_valid():
            username = registration_form.cleaned_data['username']
            first_name = registration_form.cleaned_data['first_name']
            last_name = registration_form.cleaned_data['last_name']
            email = registration_form.cleaned_data['email']
            password1 = registration_form.cleaned_data['password1']
            phone_number = registration_form.cleaned_data['phone_number']
            photo = registration_form.cleaned_data['photo']
            selected_subjects = teacher_registration_form.cleaned_data['name']

            with transaction.atomic():
                # Create a new user account
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password1)

                # Create a new profile
                if photo:
                    profile = Profile.objects.create(user=user, phone_number=phone_number, photo=photo, account_type='Teacher')
                else:
                    profile = Profile.objects.create(user=user, phone_number=phone_number, account_type='Teacher')

                # Create a new teacher account
                teacher = Teacher.objects.create(user=profile)
                teacher.lesson_type.set(selected_subjects)

            return super().form_valid(form)
        else:
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(self.request, error)

            return self.render_to_response(self.get_context_data(registration_form=registration_form, teacher_registration_form=teacher_registration_form))

    def form_invalid(self, form):
        registration_form = RegistrationForm(self.request.POST, self.request.FILES)
        teacher_registration_form = TeacherRegistrationForm(self.request.POST, self.request.FILES)

        for field_errors in form.errors.values():
            for error in field_errors:
                messages.error(self.request, error)

        return self.render_to_response(self.get_context_data(registration_form=registration_form, teacher_registration_form=teacher_registration_form))
    
    def test_func(self):
        return staff_check(self.request.user)

    def handle_no_permission(self):
        raise PermissionDenied()

class StudentRegisterView(UserPassesTestMixin, FormView):
    template_name = 'registration.html'
    success_url = reverse_lazy('registration_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registration_form'] = RegistrationForm()
        context['student_registration_form'] = StudentRegistrationForm()
        context['view_name'] = 'register_student'
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return StudentRegistrationForm(self.request.POST, self.request.FILES)

    def form_valid(self, form):
        registration_form = RegistrationForm(self.request.POST, self.request.FILES)
        student_registration_form = StudentRegistrationForm(self.request.POST, self.request.FILES)

        if registration_form.is_valid() and student_registration_form.is_valid():
            username = registration_form.cleaned_data['username']
            first_name = registration_form.cleaned_data['first_name']
            last_name = registration_form.cleaned_data['last_name']
            email = registration_form.cleaned_data['email']
            password1 = registration_form.cleaned_data['password1']
            phone_number = registration_form.cleaned_data['phone_number']
            photo = registration_form.cleaned_data['photo']
            parent = student_registration_form.cleaned_data['parent']
            class_unit = student_registration_form.cleaned_data['class_unit']



            with transaction.atomic():
                # Create a new user account
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password1)

                # Create a new profile
                if photo:
                    profile = Profile.objects.create(user=user, phone_number=phone_number, photo=photo, account_type='Student')
                else:
                    profile = Profile.objects.create(user=user, phone_number=phone_number,  account_type='Student')

                # Create a new student account
                student = Student.objects.create(user=profile, class_unit=class_unit, parent=parent )

            return super().form_valid(form)
        
        else:
            
            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(self.request, error)

            return self.render_to_response(self.get_context_data(registration_form=registration_form, student_registration_form=student_registration_form))

    def form_invalid(self, form):
        registration_form = RegistrationForm(self.request.POST, self.request.FILES)
        student_registration_form = StudentRegistrationForm(self.request.POST, self.request.FILES)

        for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(self.request, error)

        return self.render_to_response(self.get_context_data(registration_form=registration_form, student_registration_form=student_registration_form))
    
    def test_func(self):
        return staff_check(self.request.user)

    def handle_no_permission(self):
        raise PermissionDenied()

class EditUserDataView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
     
        context = {
            "profile_form": profile_form,
            "user_form": user_form,
        }
        return render(request, 'edit_profile.html', context)

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully.")
        
        else:

            for field_errors in user_form.errors.values():
                for error in field_errors:
                    messages.error(self.request, error)
            
            for field_errors in profile_form.errors.values():
                for error in field_errors:
                    messages.error(self.request, error)
        
        context = {
            "profile_form": profile_form,
            "user_form": user_form,
        }
        return render(request, 'edit_profile.html', context)
    
    

class CustomPaswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "password_change_form.html"
    success_url = reverse_lazy("passwordChangeDone")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field.capitalize()}: {error}")
        return super().form_invalid(form)

class CustomPaswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = "password_change_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context