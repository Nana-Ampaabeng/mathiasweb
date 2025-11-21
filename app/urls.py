
from django.urls import path, include 
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

 path('',views.home,name="home"),
 path('about/',views.about_page,name="about"),
 path('appointment/',views.appointment_view,name="appointment"),
 path('services/',views.service_view,name="services"),
 path('apply/',views.apply_job,name="apply"),
 path('our-team/',views.our_team,name="our-team"),
 path('depatements/',views.departments_page,name="department"),
 path('get-department-info/<int:dept_id>/', views.get_department_info, name='get_department_info'),
 path('login/', views.loginview, name='login'),
 path('logout/',views.logout_view,name="logout"),
 path('hr_dashboard/',views.HR_views,name="hr_dashboard"),
 path('nurse_app/',views.nurese_applications,name="nurse_app"),
 path('other_app/',views.others_applications,name="other_app"),
 path('events-news/',views.Event_new,name="events-news"),
    # reset password urls 
      path('password_reset/',views.CustomPasswordResetView.as_view( 
         template_name='reset_password.html',
         email_template_name="email_reset_password.html", 
         html_email_template_name="email_reset_password.html",
     ),name='password_reset'),  
    
    
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(
         template_name="reset_password_done.html",
     ),name="password_reset_done"),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
         template_name="reset_password_confirm.html"
     ),name="password_reset_confirm"),

    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(
          template_name="reset_password_complete.html"  
     ),name='password_reset_complete'),


]


