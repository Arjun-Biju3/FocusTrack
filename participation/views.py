from django.shortcuts import render

def home(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def login_user(request):
    return render(request,'login.html')

def signin_user(request):
    return render(request,'signin.html')

def courses(request):
    return render(request,'courses.html')

