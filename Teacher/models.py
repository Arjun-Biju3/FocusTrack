from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    fname = models.CharField(max_length=50, null=False)
    lname = models.CharField(max_length=50, null=False)
    subject = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=15, default=None)
    user = models.OneToOneField(User, related_name='teacher_profile', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fname} {self.lname}"
