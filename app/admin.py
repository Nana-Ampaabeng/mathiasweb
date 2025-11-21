from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin 

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display=('username','first_name','last_name','role','phone_number','is_superuser',)  
    search_fields=('username','phone_number','first_name','last_name',) 

    fieldsets=(
        (None,{'fields':('username','password')}),
        ('Personal Info',{'fields':('phone_number','first_name','last_name','role','email')}), 
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),

    )


    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('username', 'first_name','last_name','email','phone_number','role', 'password1', 'password2', 'is_staff', 'is_active',),
    }),
)


    ordering=('username',) 

admin.site.register(CustomUser,CustomUserAdmin)
 

admin.site.register(Services) 
admin.site.register(Testimonial) 
admin.site.register(Department) 
admin.site.register(SpecialWorkers) 
admin.site.register(AddRole) 
admin.site.register(Subscribes) 
admin.site.register(Announcement) 
admin.site.register(JobAlert) 

@admin.register(Appointement)
class StaffImg(admin.ModelAdmin):
    list_display=('full_name','date','phone_number')  

@admin.register(AddStaffImage)
class StaffImg(admin.ModelAdmin):
    list_display=('staff_name','staff_position','department')

@admin.register(JobApplications)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display=('sector','first_name','last_name','date') 


@admin.register(OurTeam)
class OurteamAdmin(admin.ModelAdmin):
    list_display=('team_type','name','position',)  
    
admin.site.register(departments_pages_info) 


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display=('Title','event_date','poster',)  
    
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display=('Title','news_date','poster',)    
    

    
