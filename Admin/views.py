from participation.models import *
from Teacher.models import *
from django.contrib import messages
from django.shortcuts import render,redirect
from Admin.mail import *

def admin_home(request):
    return render(request,'admin.html')

def view_students(request):
    data=profile.objects.all()
    context={'students':data}
    return render(request,'students.html',context)

def teachers_list(request):
    data = Teacher.objects.all()
    context = {'teachers':data}
    return render(request,'teachers.html',context)

def add_course(request):
    return render(request,'add_courses.html')

def add_teacher(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        phone = request.POST.get('phone')

        # Create user and teacher
        user = User.objects.create(username=email, email=email,is_staff =True)
        teacher = Teacher.objects.create(fname=fname, lname=lname, subject=subject, phone=phone, user=user)
        password = generate_random_password()
        send_email(email,password)
        messages.success(request, "Teacher added successfully!")
        return redirect('teachers_list') 
    return render(request,'add_teacher.html')