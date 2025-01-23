from django.urls import path
from participation import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about',views.about,name='about'),
    path('login',views.login_user,name='login'),
    path('signin',views.signin_user,name='signin'),
    path('courses',views.courses,name='courses'),
]
