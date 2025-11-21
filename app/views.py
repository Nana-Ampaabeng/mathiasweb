from django.shortcuts import render,redirect
from django.http import JsonResponse
import random
from django.contrib import messages
from django.urls import NoReverseMatch, reverse 
from .models import *
from .forms import * 
from django.contrib.auth import authenticate, login,logout
from django.core.paginator import Paginator 
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.mail import EmailMessage,send_mass_mail,BadHeaderError,send_mail
import smtplib   
from datetime import datetime
from django.utils.timezone import make_aware
from django.contrib.auth import get_user_model 
from django.contrib.auth.views import PasswordResetView 
from  django.urls import reverse_lazy 
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.db.models import Q 
from django.core.cache import cache

# Create your views here.
User= get_user_model() 

class CustomPasswordResetView(PasswordResetView):
    template_name = 'reset_password.html'
    email_template_name = "email_reset_password.html"
    success_url = reverse_lazy('password_reset_done')  

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
          
            return super().form_valid(form)
        else:
           
            messages.error(self.request, "Email does not match any account")
            return self.form_invalid(form)


def base(request):
    return render (request,'base.html')


def home(request): 
    events = Event.objects.only('image', 'Title', 'event_des', 'event_date','poster').first() 
    news = News.objects.only('image', 'Title', 'news_date','poster','desc').first() 
    services= Services.objects.only('Icon','Title','info')
    context={
        'services':services,
        'n':news,
        'e':events 
    } 

    return render(request,'index.html',context) 


def about_page(request):
    departments= cache.get('departments') 
    services=cache.get('services')  

    if not departments: 
        departments = list(Department.objects.all() )
        cache.set('departments',departments,60)
    if not services:  
        services =   list(AddStaffImage.objects.all()) 
        cache.set('services',services,60)    
    paginator=Paginator(services,8)     
    page_no=request.GET.get('page')     
    pagination_obj=paginator.get_page(page_no)
    # random.shuffle(pagination_obj)    
    return render(request, 'gallery.html', {'departments': departments, 'images': pagination_obj})


# appointment_view
def appointment_view(request):
    if request.method == 'POST': 
        form = AppointmentForm(request.POST)
        if form.is_valid():   
            appointment_date=form.cleaned_data['date'] 
            
            complain=form.cleaned_data['Complain']
            appointment = form.save(commit=False) 
            try:                            
                    subject = "New Appointment"
                    message = f"""
                    Hi Drs, a new appointment has been booked on {appointment_date}.
                    Complain: {complain}
                    """
                    from_mail = f"Mathias <{settings.EMAIL_HOST_USER}>"
                    to_mail = CustomUser.objects.filter(role__new_role="Doctor").values_list('email', flat=True)
                        
                    send_mass_mail(
                        (subject, message, from_mail, [recipients])
                        for recipients in to_mail
                    )

            except BadHeaderError as e:
                messages.error(request,f"Error occur when sending mail{e}")
                return redirect('appointment')
            except smtplib.SMTPException as e:
                  messages.error(request,f"Error occur when sending mail{e}")
                  return redirect('appointment')
            except Exception as e:
                 messages.error(request,f"Error occur when sending mail{e}")
                 return redirect('appointment')
            appointment.save()
            messages.success(request, f'Appointment booked successfully!')
            return redirect('appointment')
        else:     
            messages.error(request, 'Please correct the errors below.')
    else:  
        form = AppointmentForm()
    
    return render(request, 'appointment.html',{'form':form} )

# service page
def service_view(request):
    services=Services.objects.all().order_by('-id') 
    paginator=Paginator(services,6) 
    page_no=request.GET.get('page')
    page_obj=paginator.get_page(page_no) 
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'service_lists.html', {'services': page_obj})
    
    return render(request,'services.html',{'services': page_obj})


# job page 
def apply_job(request):
    if request.method == "POST": 
        forms = JobapplicationForms(request.POST, request.FILES)
        if forms.is_valid(): 
            first_name = forms.cleaned_data['first_name']
            email = forms.cleaned_data['email'] 
            forms.save() 
            try:         
                send_mail(
                    subject="Mathias Job Applications", 
                    message=f"Thank you {first_name}, we will get back to you!",
                    from_email=f"Mathias Hospital<{settings.EMAIL_HOST_USER}>",
                    recipient_list=[email],   
                    fail_silently=False 
                )
                messages.success(request, "Your application was submitted successfully ")
                return redirect('apply')  

            except BadHeaderError as e:
                messages.error(request,f"Error occur {e}") 
                return redirect('apply')
            except smtplib.SMTPException as e: 
                messages.error(request,f'Error Occur {e}')
                return redirect('apply')
            except Exception as e: 
                messages.error(request,f'Error Occur {e}')
                return redirect('apply')
        else: 
            messages.error(request,"Error Occur when submitting forms. Try again")
            return redirect('apply')
    else: 
        allow_job=JobAlert.objects.filter(allow="Allow") 
        forms = JobapplicationForms()   
        return render(request,'jobs.html',{'form':forms}) 


# OUT TEAM PAGE 

def our_team(request):
     Management_Team= cache.get('management_team')
     Department_Team=cache.get('department_team')


     if not Management_Team: 
        Management_Team=list(OurTeam.objects.filter(team_type="Management_Team"))
        cache.set('management_team', Management_Team,60)

     if not Department_Team:
        Department_Team=list(OurTeam.objects.filter(team_type="Department_team")) 
        cache.set('department_team', Department_Team,60)

     context={  
          'mt':Management_Team,   
          'dt':Department_Team 
     } 
     return render(request,'ourteam.html',context) 


# dapartment page 
def departments_page(request):
    departments = Department.objects.all()
    # Get the first department as default
    default_dept = departments.first()
    default_info = departments_pages_info.objects.filter(department=default_dept).first()
        
    context = {
        'departments': departments,
        'default_department': default_dept,
        'default_info': default_info,
    }
    return render(request, 'departments.html',context)


def get_department_info(request, dept_id):
    try:
        department = Department.objects.get(id=dept_id)
        info = departments_pages_info.objects.filter(department=department).first()

        data = {
            'department_name': department.Name,
            'image1': info.image1.url if info.image1 else '',
            'image2': info.image2.url if info.image2 else '',
            'image3': info.image3.url if info.image3 else '',
            'in_charge_img': info.in_charge_img.url if info.in_charge_img else '',
            'in_charge_name': info.in_charge_name,
        }
        return JsonResponse(data)
    except Department.DoesNotExist:
        return JsonResponse({'error': 'Department not found'}, status=404)


# HR VIEWS
def HR_views(request):
    # Get all applications
    applications = JobApplications.objects.all().order_by('-date')
    sectors_filter= request.GET.get('sectors') 
    date_filter=request.GET.get('date')
    query=request.GET.get('q','')

    if query:
         applications=JobApplications.objects.filter(
              Q(first_name__icontains=query) | Q(last_name__icontains=query)
         )

    if sectors_filter:
         applications=JobApplications.objects.filter(sector=sectors_filter) 

    if date_filter:
        applications=JobApplications.objects.filter(date__date=date_filter) 


    # Calculate statistics
    total_applications = applications.count()
    nurse_applications = applications.filter(sector='Nurse').count()
    other_applications = applications.filter(sector='Others').count()

    # Applications this month
    start_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_applications = applications.filter(date__gte=start_of_month).count()
    
    context = {
        'applications': applications,
        'total_applications': total_applications,
        'nurse_applications': nurse_applications,
        'other_applications': other_applications,
        'monthly_applications': monthly_applications,
    }
    
    return render(request, 'HR_dashboard.html', context) 

def nurese_applications(request):
    get_nures_app=JobApplications.objects.filter(sector="Nurse")
    return render(request,'nurse_application.html',{'appointment':get_nures_app}) 


def others_applications(request):       
    get_other_app=JobApplications.objects.filter(sector="Others")
    return render(request,'other_application.html',{'appointments':get_other_app}) 


# logined view 
def loginview(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            role_name = user.role.new_role if user.role else None

            if request.user.is_superuser:
                return redirect('/admin/')

            elif role_name == "Doctor":
                return redirect('doctor_page')

            elif role_name == "Student":
                return redirect('student_dashboard')
            
            elif role_name == "HR":
                return redirect('hr_dashboard')

            else: 
                return redirect('foolish.html')  

        else:
            messages.error(request, "Invalid username or password")
            return redirect('login') 

    return render(request, 'login.html')

# logout
def logout_view(request):
    logout(request)
    messages.info(request,'Logout successfully') 
    return redirect('home')


# event and new 
def Event_new(request):
    events = Event.objects.only('image', 'Title', 'event_des', 'event_date','poster') 
    news = News.objects.only('image', 'Title', 'news_date','poster','desc') 
    return render(request, 'event_new.html', {'events': events,'news':news}) 


# def readmoreDetails(request,id):
#     eventd=Event.objects.get(id=id)
#     newsd=News.objects.get(id=id) 
