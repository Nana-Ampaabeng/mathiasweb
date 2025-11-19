from django.shortcuts import render

# Create your views here.


def base(request):
    return render (request,'base.html')


def home(request): 
    return render(request,'index.html')


def about_page(request):
    return render(request,'gallery.html')

# appointment_view
def appointment_view(request):
    # if request.method == 'POST': 
    #     form = AppointmentForm(request.POST)
    #     if form.is_valid():   
    #         appointment_date=form.cleaned_data['date'] 
            
    #         complain=form.cleaned_data['Complain']
    #         appointment = form.save(commit=False) 
    #         try:                            
    #                 subject = "New Appointment"
    #                 message = f"""
    #                 Hi Drs, a new appointment has been booked on {appointment_date}.
    #                 Complain: {complain}
    #                 """
    #                 from_mail = f"Mathias <{settings.EMAIL_HOST_USER}>"
    #                 to_mail = CustomUser.objects.filter(role__new_role="Doctor").values_list('email', flat=True)
                        
    #                 send_mass_mail(
    #                     (subject, message, from_mail, [recipients])
    #                     for recipients in to_mail
    #                 )

    #         except BadHeaderError as e:
    #             messages.error(request,f"Error occur when sending mail{e}")
    #             return redirect('appointment')
    #         except smtplib.SMTPException as e:
    #               messages.error(request,f"Error occur when sending mail{e}")
    #               return redirect('appointment')
    #         except Exception as e:
    #              messages.error(request,f"Error occur when sending mail{e}")
    #              return redirect('appointment')
    #         appointment.save()
    #         messages.success(request, f'Appointment booked successfully!')
    #         return redirect('appointment')
    #     else:     
    #         messages.error(request, 'Please correct the errors below.')
    # else:  
    #     form = AppointmentForm()
    
    return render(request, 'appointment.html', )

# service page
def service_view(request):
    # services=Services.objects.all().order_by('-id') 
    # paginator=Paginator(services,6) 
    # page_no=request.GET.get('page')
    # page_obj=paginator.get_page(page_no) 
    # if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #     return render(request, 'service_lists.html', {'services': page_obj})
    
    return render(request,'services.html',)


# job page 
def apply_job(request):
    # if request.method == "POST": 
    #     forms = JobapplicationForms(request.POST, request.FILES)
    #     if forms.is_valid(): 
    #         first_name = forms.cleaned_data['first_name']
    #         email = forms.cleaned_data['email'] 
    #         forms.save() 
    #         try:         
    #             send_mail(
    #                 subject="Job Applications Successfully",
    #                 message=f"Thank you {first_name}, we will get back to you!",
    #                 from_email=f"Mathias Hospital<{settings.EMAIL_HOST_USER}>",
    #                 recipient_list=[email],   
    #                 fail_silently=False 
    #             )
    #             messages.success(request, "Your application was submitted successfully ")
    #             return redirect('jobs')  

    #         except BadHeaderError as e:
    #             messages.error(request,f"Error occur {e}") 
    #             return redirect('jobs')
    #         except smtplib.SMTPException as e: 
    #             messages.error(request,f'Error Occur {e}')
    #             return redirect('jobs')
    #         except Exception as e: 
    #             messages.error(request,f'Error Occur {e}')
    #             return redirect('jobs')
    #     else: 
    #         messages.error(request,"Error Occur when submitting forms. Try again")
    #         return redirect('jobs')
    # else: 
    #     allow_job=JobAlert.objects.filter(allow="Allow") 
    #     forms = JobapplicationForms()   
        return render(request,'jobs.html') 


# OUT TEAM PAGE 

def our_team(request):
     
    #  Management_Team= cache.get('management_team')
    #  Department_Team=cache.get('department_team')


    #  if not Management_Team: 
    #     Management_Team=list(OurTeam.objects.filter(team_type="Management_Team"))
    #     cache.set('management_team', Management_Team,60)

    #  if not Department_Team:
    #     Department_Team=list(OurTeam.objects.filter(team_type="Department_team")) 
    #     cache.set('department_team', Department_Team,60)

    #  context={  
    #       'mt':Management_Team,   
    #       'dt':Department_Team 
    #  } 
     return render(request,'ourteam.html') 


# dapartment page 
def departments_page(request):
    # departments = Department.objects.all()
    # # Get the first department as default
    # default_dept = departments.first()
    # default_info = departments_pages_info.objects.filter(department=default_dept).first()
        
    # context = {
    #     'departments': departments,
    #     'default_department': default_dept,
    #     'default_info': default_info,
    # }
    
    return render(request, 'departments.html')


