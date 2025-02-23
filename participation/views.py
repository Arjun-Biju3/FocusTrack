from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from participation.models import *
from participation.otp import *
import socket
from django.contrib import messages
from datetime import datetime,timedelta
from django.utils import timezone
import os
from django.conf import settings
import cv2
import numpy as np
from PIL import Image
import base64
from io import BytesIO
from django.contrib.auth import authenticate,login,logout
from django.core.files.base import ContentFile
import subprocess
import datetime
from participation.distraction_detection import *

db_dir = os.path.join(settings.BASE_DIR, 'db')
if not os.path.exists(db_dir):
    os.mkdir(db_dir)


def decode_image(image_data):
    image_data = image_data.split(',')[1]
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return image

def home(request):
    if request.method == 'POST':
        username = request.user.username 
        image_data = request.POST.get('image')
        folder_name = username
        folder_path = os.path.join(db_dir, folder_name)
        log_path = os.path.join(folder_path, 'log.txt')
        unknown_img_path = os.path.join(folder_path, '.tmp.jpg')
            
        try:
            image_data = image_data.split(',')[1]
            image = Image.open(BytesIO(base64.b64decode(image_data)))
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv2.imwrite(unknown_img_path, image)
            
            # prediction, scores = predict_distraction()
            # with open(log_path, 'a') as f:
            #     f.write(f'{prediction} {datetime.datetime.now()}\n') 
            
            if not image_data:
                print("image not found")
                
            #run recognition
            output = subprocess.check_output(['face_recognition', folder_path, unknown_img_path])
            output = output.decode('utf-8').strip()
            name = output.split(',')[1] if ',' in output else 'unknown'
            print(name)
            if name in ['unknown_person', 'no_persons_found', 'unknown']:
                print(name)
                with open(log_path, 'a') as f:
                    f.write(f'{name},Not active,{datetime.datetime.now()}\n')
            elif name == username:
                #run distraction detection
                prediction, scores = predict_distraction(username=username)
                if prediction is not None:
                    print(f"Prediction: {prediction}, Scores: {scores}")
                with open(log_path, 'a') as f:
                    f.write(f'{name},Active,{datetime.datetime.now()}\n')
                    f.write(f'{prediction},Active,{datetime.datetime.now()}\n')  
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if os.path.exists(unknown_img_path):
                os.remove(unknown_img_path)
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def login_user(request):
    if request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                return redirect('admin_home')                
            else:
                login(request,user)
                return redirect('home')
        else:
            messages.error(request,"Invalid username or password")
    return render(request,'login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def capture(request):
    if request.method == 'POST':
        #capture image and save
        username = request.session.get('email')  
        image_data = request.POST.get('image')
        image = decode_image(image_data)
        user_dir = os.path.join(db_dir, username)
        os.makedirs(user_dir, exist_ok=True)
        filename = os.path.join(user_dir, f'{username}.jpg')
        cv2.imwrite(filename, image)
        #fetch user details
        fname=request.session.get('fname')
        lname=request.session.get('lname')
        gender=request.session.get('gender')
        country=request.session.get('country')
        program=request.session.get('program')
        phone=request.session.get('phone')
        email=request.session.get('email')
        password=request.session.get('password')
        #create user
        request.session.flush()
        user=User.objects.create_user(username=email,password=password,email=email)
        profile.objects.create(fname=fname,lname=lname,geder=gender,country=country,program=program,phone=phone,user=user)
        #login user
        user=authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"error in logging")
            return redirect('login')
    return render(request, 'capture_image.html')

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