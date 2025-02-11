from django.urls import path
from Admin import views

urlpatterns = [
   path('admin_home',views.admin_home,name='admin_home'),
   path('view_students',views.view_students,name='view_students'),
   
]
