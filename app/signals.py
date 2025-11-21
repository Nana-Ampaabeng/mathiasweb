from .models import Subscribes, Announcement,OurTeam,departments_pages_info,Department,AddStaffImage
from django.db.models.signals import post_save ,post_delete
from django.dispatch import receiver
from django.conf import settings 
from django.core.mail import send_mass_mail,send_mail  
from django.core.cache import cache 

@receiver(post_save, sender=Announcement)
def sendAccoucement_To_Subscribers(sender,created,instance,**kwargs):
    if created:
        subject=instance.Title,
        message=instance.message 
        from_mail=f"Mathias <{settings.EMAIL_HOST_USER}>", 

        all_subscribers=Subscribes.objects.all() 
        for emails in all_subscribers:

            send_mail(subject,message,from_mail,[emails],fail_silently=False) 
            

@receiver(post_save, sender=OurTeam)
def clear_cache_add(sender,**kwargs):
    cache.delete('management_team')
    cache.delete('department_team')
    print("delted correctly") 


@receiver(post_delete, sender=OurTeam) 
def clear_cache_delte(sender, **kwars):
    cache.delete('depatment_team') 
    cache.delete('management_team')  
    print("upadate cache when deleted")


@receiver(post_save, sender=departments_pages_info) 
def clear_cache_delte(sender, **kwars):
    cache.delete('images')  
    print("d image save")


    # department page
@receiver(post_delete, sender=departments_pages_info) 
def clear_cache_delte(sender, **kwars):
    cache.delete('images') 
     
    print("images deleted")



@receiver(post_save,sender=AddStaffImage)  
def clear_cache_delte(sender, **kwars):
    cache.delete('images') 
    print("StaffImage deleted")


@receiver(post_delete, sender=AddStaffImage) 
def clear_cache_delte(sender, **kwars):
    cache.delete('images') 
    print("staffImages deleted")


@receiver(post_save,sender=Department)  
def clear_cache_delte(sender, **kwars):
    cache.delete('images') 
    print("images deleted")


@receiver(post_delete, sender=AddStaffImage) 
def clear_cache_delte(sender, **kwars):
    cache.delete('images') 
    print("images deleted")
