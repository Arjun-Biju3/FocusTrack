from django.urls import path
from participation import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about',views.about,name='about'),
    path('login',views.login_user,name='login'),
]
