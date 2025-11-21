from django import forms
from .models import Testimonial,CustomUser,JobApplications
from .models import Appointement
from django.core.validators import MinValueValidator
from datetime import date, datetime
import re
from django.contrib.auth.forms import UserCreationForm



class Registration(UserCreationForm):
    class Meta:
        model=CustomUser 
        fields=['username','email','phone_number','role','password1','password2',]

        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'phone_number':forms.TextInput(attrs={'class':'form-control'}),
            'role':forms.Select(attrs={'class':'form-select'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control'}),
            
        }






class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'email', 'message','pic' ] 
        labels={
            'email':"Email(Optional)",
            'pic':"Your Pic (Optional)"
        }
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'pic': forms.FileInput(attrs={'class': 'form-control'}), 
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'place holder': 'Your Feedback...'}),
        } 



class AppointmentForm(forms.ModelForm):
    # Add custom validation and widgets for better UX
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'pattern': '[0-9]{10,15}',
            'title': 'Please enter a valid phone number (10-15 digits)',
            'class':"form-control",
            'placeholder':'Your phone number'
        })
    )
    
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date','class':'form-control'}),
        validators=[MinValueValidator(date.today())]
    )
    
    # time = forms.TimeField(
    #     widget=forms.TimeInput(attrs={'type': 'time','class':'form-control'})
    # )
     
    class Meta:
        model = Appointement 
        fields = ['full_name', 'email', 'date', 'phone_number', 'Complain','Gender']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'placeholder': 'Enter your full name',
                'class': 'form-control' 
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email address',
                'class': 'form-control'
            }),
            'Complain': forms.Textarea(attrs={
                'placeholder': 'Describe your symptoms or reason for appointment',
                'rows': 4,
                'class': 'form-control'
            }), 

            'Gender': forms.Select(attrs={
                'placeholder': 'Gender', 
                'class': 'form-select'
            }),


        }
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        # Remove any non-digit characters
        phone_number = re.sub(r'\D', '', phone_number)
        
        if len(phone_number) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits long.")
        
        return phone_number
    
    def clean_date(self):
        appointment_date = self.cleaned_data['date']
        if appointment_date < date.today():
            raise forms.ValidationError("Appointment date cannot be in the past.")
        return appointment_date






class JobapplicationForms(forms.ModelForm):
    class Meta: 
        model=JobApplications
        fields=['sector','first_name','last_name','email','url','resume','cover_letter','about_us']  

        widgets={
            'sector':forms.Select(attrs={'class':'form-select'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'firstname'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'lastname'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
            'url':forms.URLInput(attrs={'class':'form-control','placeholder':'for eg. linkedin,twitter,facebook'}),
            'resume':forms.FileInput() ,
            'cover_letter':forms.FileInput() ,
            'about_us':forms.TextInput(attrs={'class':'form-control'})
        }    

