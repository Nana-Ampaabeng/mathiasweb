
from django.urls import path, include 
from . import views

urlpatterns = [

 path('',views.home,name="home"),

 path('about/',views.about_page,name="about"),
 path('appointment/',views.appointment_view,name="appointment"),
 path('services/',views.service_view,name="services"),
 path('apply/',views.apply_job,name="apply"),
 path('our-team/',views.our_team,name="our-team"),
 path('depatements/',views.departments_page,name="department"),

]


