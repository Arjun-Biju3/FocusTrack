from django.urls import path
from Admin import views

urlpatterns = [
   path('admin_home',views.admin_home,name='admin_home'),
   path('view_students',views.view_students,name='view_students'),
   path('teachers_list',views.teachers_list,name='teachers_list'),
   path('add_course',views.add_course,name='add_course')
   
]
