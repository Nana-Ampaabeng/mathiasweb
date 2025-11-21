from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings 

# Create your models here.
class AddRole(models.Model):
    new_role=models.CharField(max_length=50)
    
    def __str__(self):
        return self.new_role

class CustomUser(AbstractUser): 
    role= models.ForeignKey(AddRole,on_delete=models.CASCADE,null=True, blank=True)  
    phone_number=models.PositiveIntegerField(null=True,blank=True) 


class Department(models.Model):
    Name=models.CharField(max_length=50)  
    def __str__(self):
        return self.Name 


class departments_pages_info(models.Model):
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    image1=models.ImageField(upload_to='upload/departments_pages_img1',blank=True, null=True)
    image2=models.ImageField(upload_to='upload/departments_pages_img2',blank=True, null=True)
    image3=models.ImageField(upload_to='upload/departments_pages_img3',blank=True, null=True)
    in_charge_img=models.ImageField(upload_to='upload/inchargeimages')
    in_charge_name=models.CharField(max_length=50)

    def __str__(self):
        return f"{self.department} {self.in_charge_name}"
    
import secrets,string 
def secure_reference_code(length=10):
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))
  

class Appointement(models.Model): 
    full_name=models.CharField(max_length=50) 
    email=models.EmailField()  
    date=models.DateField() 
    phone_number=models.PositiveIntegerField() 
    Complain=models.TextField() 
    Doctor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, blank=True, null=True)

    Gender=models.CharField(max_length=50, choices=[
        ("","Choose"),
        ("male","Male"),
        ("female","Female"), 
    ],default="choose") 
 
    Status=models.CharField(max_length=50, choices=[
        ("pending","Pending"),
        ("approved","Approved"), 
        ("complete","Complete"), 
        ("cancelled","Cancelled"),  
    ],default="pending")  
    refrence=models.CharField(max_length=10,null=True,blank=True,unique=True,default=None)   
    def __str__(self):
        return self.full_name  
    
    def save(self,*args,**kwargs):
        if not self.refrence:
            self.refrence= secure_reference_code() 
        super().save(*args,**kwargs) 



class Services(models.Model):
    Icon=models.ImageField(upload_to='uploads/Service Icons/', blank=True,null=True) 
    Title=models.CharField(max_length=50)  
    info=models.TextField() 
    def __str__(self):
        return self.Title
    class Meta:
        verbose_name="Service"

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    pic=models.ImageField(upload_to='uploads/testify', null=True,blank=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approve=models.BooleanField(default=False)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} {self.approve}"
    



class AddStaffImage(models.Model):
    staff_name=models.CharField(max_length=50) 
    staff_position=models.CharField(max_length=50) 
    staff_pic=models.ImageField(upload_to="uploads/staffImages",blank=True,null=True) 
    department=models.ForeignKey(Department,on_delete=models.CASCADE) 
    def __str__(self):
        return self.staff_name 
    class Meta:
        verbose_name="About U" 

class SpecialWorkers(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='doctors/')
    
    def __str__(self):
        return self.name
    

class Subscribes(models.Model):
    emails=models.EmailField() 

    def __str__(self):
        return self.emails
    
class Announcement(models.Model):
    Title=models.CharField(max_length=50) 
    message=models.TextField() 

    def __str__(self):
        return self.Title 


class JobApplications(models.Model): 
    sector=models.CharField(max_length=50,  choices=[
        ("","--Apply for--"),
        ("Nurse","nurse"),
        ("Others","others"), 
    ],default="--Apply for--")

    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50) 
    email=models.EmailField() 
    url=models.URLField()    
    date=models.DateTimeField(auto_now_add=True)
    resume=models.FileField(upload_to='uploads/job_applications')
    cover_letter=models.FileField(upload_to='uploads/Cover_letters') 
    about_us=models.TextField(max_length=100) 

    def __str__(self):
        return self.sector 

    

class JobAlert(models.Model):
    allow=models.CharField(choices=[
         ("Allow","Allow"),
         ("Disable","Disable"),
     ], max_length=50
      ) 
    
    def __str__(self):
        return self.allow  
    class Meta:
        verbose_name="Allow Job"


class OurTeam(models.Model):
    team_type = models.CharField(
        choices=[
            ("Department_team","Department_team"),
            ("Management_Team","Management_Team"),
        ], default="Choice", max_length=50
        ) 
    name = models.CharField(max_length=50) 
    position = models.CharField(max_length=50)
    image = models.ImageField(upload_to='team_images/', blank=True, null=True)
    
    def __str__(self):
        return self.name 


class Event(models.Model):
    image=models.ImageField(upload_to='event/', blank=True,null=True)
    Title=models.CharField(max_length=50)
    event_des=models.TextField() 
    event_date=models.DateTimeField(auto_created=False,) 
    poster=models.CharField(max_length=50, null=True,blank=True) 
    def __str__(self):
        return self.Title 
    

class News(models.Model):
    image=models.ImageField(upload_to="news/",blank=True,null=True) 
    news_date=models.DateTimeField(auto_created=False)
    Title=models.CharField(max_length=50) 
    desc=models.TextField()
    poster=models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.Title  
    


