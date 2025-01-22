from django.urls import path
from participation import views

urlpatterns = [
    path('',views.home,name='home')
]
