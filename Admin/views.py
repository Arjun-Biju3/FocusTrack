from participation.models import *


from django.shortcuts import render

def admin_home(request):
    return render(request,'admin.html')

def view_students(request):
    data=profile.objects.all()
    context={'students':data}
    return render(request,'students.html',context)

def teachers_list(request):
    return render(request,'teachers.html')

def add_course(request):
    return render(request,'add_courses.html')