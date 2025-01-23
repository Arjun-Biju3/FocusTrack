from django.db import models
from django.contrib.auth.models import User

class profile(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES=((LIVE,'Live'),(DELETE,'Delete'))
    fname=models.CharField(max_length=10,null=False)
    lname=models.CharField(max_length=10,null=False)
    geder=models.CharField(max_length=10)
    country=models.CharField(max_length=20)
    program=models.CharField(max_length=20)
    phone=models.CharField(max_length=15,default=None)
    user=models.OneToOneField(User,related_name='user_profile',on_delete=models.CASCADE)
    delete_status=models.IntegerField(choices=DELETE_CHOICES,default=LIVE)
    created_at=models.DateTimeField(auto_now_add=True)
