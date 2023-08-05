from django.shortcuts import render,redirect
from messagesApp.models import Message
from .models import Grades, Semester
from usersApp.models import Student, ClassUnit, Profile
from eventApp.models import Teacher, Subject
from django.shortcuts import get_object_or_404
from calendarApp.forms import ClassUnitForm
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def view_grades(request, semester=None):


    if not semester:
            semester = Semester.objects.last()
    else:
        try:
            semester = get_object_or_404(Semester, id=semester)
        except:
            semester = Semester.objects.last()

    if request.user.profile.account_type == 'Teacher':
        # class_id = ClassUnit.objects.last()
        pass

    elif request.user.profile.account_type == 'Student':

        student = get_object_or_404(Student, user=request.user.profile)
        grades = {subject: Grades.objects.filter(student=student, subject=subject, semester= semester) for subject in Subject.objects.all()}

    elif request.user.profile.account_type == 'Parent':
        # parent_profile = request.user.profile.parent
        # student = Student.objects.filter(parent=parent_profile).first()
        # if student:
        #     class_id = student.class_unit
        pass
    else:
        class_id = ClassUnit.objects.last()


    
    if request.method == 'GET':        

        form = ClassUnitForm()


        context={
            'grades':grades,
            'form': form,
        }

        return render(request, 'view_grades.html', context)
    else:
        form = ClassUnitForm(request.POST)

        if form.is_valid():
            class_id = form.cleaned_data['class_unit'].id
            return redirect('view_grades', class_id=class_id)