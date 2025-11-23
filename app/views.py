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
    if request.method=='POST':
         email=request.POST.get('subscribemails')  
         subcribsemail=Subscribes.objects.create(emails=email) 
         subcribsemail.save()  
         messages.info(request,'We will notify you of any update')
         return redirect('home')
    gallary=Gallary.objects.only('image','title','description')[:5]
    events = Event.objects.only('image', 'Title', 'event_des', 'event_date','poster').first() 
    news = News.objects.only('image', 'Title', 'news_date','poster','desc').last()
    services= Services.objects.only('Icon','Title','info')
    context={
        'services':services,
        'n':news,
        'e':events ,
        'g':gallary 
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
    return render(request, 'about_us.html', {'departments': departments, 'images': pagination_obj})

# gallyer page 
def gallary(request):

    gallarys=Gallary.objects.only('image','title','description')
    paginator=Paginator(gallarys,8) 
    page_no=request.GET.get('page')
    paginator_obj=paginator.get_page(page_no) 
    return render(request,'gallary.html',{'gallary':paginator_obj})



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
    return redirect('home')


# event and new 
def Event_new(request):
    events = Event.objects.only('image', 'Title', 'event_des', 'event_date','poster') 
    news = News.objects.only('image', 'Title', 'news_date','poster','desc') 
    return render(request, 'event_new.html', {'events': events,'news':news}) 


 # doctor's view appointment 
def doctor_appointments(request):
    # Get all appointments ordered by date and time
    status_filter=request.GET.get('status') 
    date_filter=request.GET.get('date')
    id_search=request.GET.get('id') 
    appointments_list = Appointement.objects.all().order_by('date')
    if id_search:  
         appointments_list=Appointement.objects.filter(refrence=id_search)
    if status_filter:   
        appointments_list=Appointement.objects.filter(Status=status_filter)
                                                                       
    if date_filter:  
        try:
            appointments_list=Appointement.objects.filter(date=date_filter)  
        except ValueError:
                messages.error(request, "Invalid date format.")
                return redirect('doctor_page') 
         
    
    
    # Pagination
    paginator = Paginator(appointments_list, 10)  
    page_number = request.GET.get('page') 
    appointments = paginator.get_page(page_number)
    
    # Calculate statistics
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    today_count = Appointement.objects.filter(date=today).count()
    week_count = Appointement.objects.filter(date__range=[start_of_week, end_of_week]).count()

    pending_count = Appointement.objects.filter(Status="pending").count()
    approve_count = Appointement.objects.filter(Status="approved").count()
    complete_count = Appointement.objects.filter(Status="complete").count()
    cancel_count = Appointement.objects.filter(Status="cancelled").count()
    total_patients = Appointement.objects.values("phone_number").distinct().count()
    
    today_appointments = Appointement.objects.filter(date=today)

    context = {
        'appointments': appointments,
        'today_appointments': today_appointments,
        'today_count': today_count,
        'week_count': week_count,
        'approved_count': approve_count,
        'complete_count': complete_count,
        'cancel_count': cancel_count, 
        'pending_count': pending_count,
        'total_patients': total_patients,
        'today': today,
        'status_filter':status_filter,  
    }
    
    return render(request, 'doctors_dashboard.html', context) 

def cancel_patient(request):
    cancel_patients=Appointement.objects.filter(Status="cancelled")
    return render(request,'cancel_patient.html',{'appointments':cancel_patients}) 

def pending_patient(request):
    get_pending_patients=Appointement.objects.filter(Status="pending")
    return render(request,'pending_patient.html',{'appointments':get_pending_patients}) 


def complete_patient(request):
    get_complete_patients=Appointement.objects.filter(Status="complete") 
    return render(request,'complete_patient.html',{'appointments':get_complete_patients}) 


def approve_patient(request):
    get_approve_patients=Appointement.objects.filter(Status="approved")
    return render(request,'approve_patient.html',{'appointments':get_approve_patients})  

def today_appointment(request):
    today = timezone.now().date()
    get_approve_patients=Appointement.objects.filter(date=today)
    return render(request,'today_appointment.html',{'appointments':get_approve_patients})  


import secrets,string
def secure_reference_code(length=10):
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

# approve appointment  
def approve_appointment(request,id): 
    try:
         patient_app_id=Appointement.objects.get(id=id) 
        
    except Appointement.DoesNotExist:
        messages.info(request,"Appointment id does't not exist")
        return redirect(request,'doctor_page')

    patient_app_id.Status="approved" 
    patient_app_id.Doctor=request.user 
    # generate refrence code 
    patient_refrence_code=secure_reference_code()
    patient_app_id.refrence=patient_refrence_code
    if Appointement.objects.filter(refrence=patient_refrence_code).exists():
        messages.error(request,'Refrence code exist already try again') 
        return redirect('doctor_page')  
        
    try: 
        sendmail=EmailMessage(
            body=f"Your Appointement have been approved by DR.{request.user} \n <h3> appointment code:{patient_refrence_code}",
            from_email=f"Mathias<{settings.EMAIL_HOST_USER}>", 
            to=[patient_app_id.email],
            bcc=["issahsalim233@gmail.com"] 
        ) 
        sendmail.send() 
    except BadHeaderError as e:
                messages.error(request,f"Error occur when sending mail. Try again : {e}")
                return redirect('doctor_page')
    
    except smtplib.SMTPException as e:
                  messages.error(request,f"Error occur when sending mail. Try again {e}")
                  return redirect('doctor_page')
            
    except Exception as e: 
        messages.error(request,f"Error occur when send mail to patient try again. error code{e}")
        return redirect('doctor_page') 
    patient_app_id.save()  
    messages.success(request,f"Appointement successfully approved by DR.{request.user}") 

    try:
        url=redirect(reverse('doctor_page'))
    except NoReverseMatch: 
        messages.error(request, "Page not found. Redirecting to dashboard instead.")
        return redirect('doctor_page') 
    return redirect('doctor_page')
    

# cancel appointment
def cancel_appointment(request, id):
        try:
            appointment = Appointement.objects.get(id=id, Doctor=request.user)
        except Appointement.DoesNotExist: 
            messages.error(request,'Appointment doest not exsit')
            return redirect('doctor_patients')
        appointment.Status = "cancelled"
        appointment.Doctor=None 
        appointment.refrence="" 
        try:  
            sendmail=EmailMessage(
                body=f"""
                        Hi, {appointment.full_name} DR.{request.user} has Cancelled you appointement with him <br/>
                        <h1> Sorry for that wait for another approval by another doctor</h1> 
                    """,  
                from_email=f"Mathias<{settings.EMAIL_HOST_USER}>",
                to=[appointment.email],
                bcc=["issahsalim233@gmail.com"] 
            )   
            sendmail.send() 
        except BadHeaderError as e:
                messages.error(request,f"Error occur when sending mail{e}")
                return redirect('doctor_patients')
    
        except smtplib.SMTPException as e:
                  messages.error(request,f"Error occur when sending mail{e}")
                  return redirect('doctor_patients')
            
        except Exception as e:  
            messages.error(request,f"Error occur when send mail to patient why again. error code{e}")
            return redirect('doctor_patients') 
        
        appointment.save() 
        messages.info(request,'Appointment cancelled') 
        return redirect('doctor_patients')  


  #complete appointment 

def complete_appointment(request, id):
        try:
            appointment = Appointement.objects.get(id=id, Doctor=request.user)
        except Appointement.DoesNotExist: 
            messages.error(request,'Appointment doest not exsit')
            return redirect('doctor_patients')
        appointment.Status = "complete"
         
        appointment.save() 
        messages.info(request,f'Appointment complete. Nice work DR.{request.user}') 
        return redirect('doctor_patients')  
        

def doctor_patients(request):
    my_patients=Appointement.objects.filter(Doctor=request.user) 
    return render(request,'doctor_page.html',{'doctor_patients':my_patients})

