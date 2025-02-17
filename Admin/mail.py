import random
import http.client
import smtplib
from email.message import EmailMessage
from datetime import datetime,timedelta
from django.http import HttpResponse
import secrets
import string

def generate_random_password(length=10):
    characters = string.ascii_letters + string.digits 
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


def send_email(username,password):
    msg=EmailMessage()
    subject="Username and password"
    body=f"Your registration is succesful and username is {username} and password is {password}.Please do not share it with any one"
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = username
    user="ivpe68030@gmail.com"
    msg['from']=user
    password="utba gpfp sfgt lagn"
     
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    server.quit()

