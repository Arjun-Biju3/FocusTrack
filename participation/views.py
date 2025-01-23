from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from participation.models import *
from participation.otp import *
import socket
from django.contrib import messages
from datetime import datetime,timedelta
from django.utils import timezone

def home(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def login_user(request):
    return render(request,'login.html')


def capture(request):
    return render(request,'capture_image.html')

def signin_user(request):
    if request.POST:
        #fetch deatails
        email=request.POST.get('email')
        request.session['fname']=request.POST.get('fname')
        request.session['lname']=request.POST.get('lname')
        request.session['email']=email
        request.session['phone']=request.POST.get('phone')
        request.session['gender']=request.POST.get('gender')
        request.session['country']=request.POST.get('country')
        request.session['program']=request.POST.get('program')
        request.session['password'] =request.POST.get('password')
        
        otp=generate_otp()
        request.session['otp'] = otp
        request.session['otp_expires'] = (datetime.now() + timedelta(minutes=5)).isoformat()
        try:
            send_email(email,otp)
            return redirect('otp')
        except socket.gaierror as e:
            messages.error(request,"please check your connection")

        
        # user=User.objects.create_user(username=email,password=password,email=email)
        # profile.objects.create(fname=fname,lname=lname,geder=gender,country=country,program=program,phone=phone,user=user)
       
    return render(request,'signin.html')

def courses(request):
    return render(request,'courses.html')

def otp(request):
    success_message="OTP has been send succesfully"
    messages.success(request,success_message)
    if request.POST:
        otp=request.POST.get('otp')
        res=validate_otp(request,otp)
        if res==1:
            clear_otp(request)
            adhar=request.session.get('adhar')
            return redirect('capture')
        if res==-1:
            error_message="OTP Expired"
            messages.error(request,error_message)
        if res==0:
            error_message="Invalid OTP"
            messages.error(request,error_message)
       #resend
    if request.POST and 'resend' in request.POST:
        otp=generate_otp()
        email=request.session.get('email')
        request.session['otp']=otp
        request.session['otp_expires'] = (datetime.now() + timedelta(minutes=5)).isoformat()
        
        send_email(email,otp)
        messages.success(request,"OTP has been send succesfully")

    return render(request,'otp.html')