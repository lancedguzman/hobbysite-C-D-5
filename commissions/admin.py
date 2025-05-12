from django.contrib import admin
from .models import Commission, Job, JobApplication

class JobInline(admin.TabularInline):  
    model = Job
    extra = 1  
    fields = ('role', 'manpower_required', 'status')  
    list_filter = ('status',)  

class JobApplicationInline(admin.TabularInline):  
    model = JobApplication
    extra = 1  
    fields = ('applicant', 'status', 'applied_on') 
    list_filter = ('status',)  

class CommissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'author', 'created_on', 'updated_on')
    search_fields = ('title', 'author__display_name')
    list_filter = ('status', 'created_on')
    inlines = [JobInline]  

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'author', 'status')  
        }),
    )

class JobAdmin(admin.ModelAdmin):
    list_display = ('commission', 'role', 'manpower_required', 'status')
    search_fields = ('role', 'commission__title')
    list_filter = ('status',)
    inlines = [JobApplicationInline] 

    fieldsets = (
        (None, {
            'fields': ('commission', 'role', 'manpower_required', 'status') 
        }),
    )

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_on')
    search_fields = ('job__role', 'applicant__display_name')
    list_filter = ('status',)

    fieldsets = (
        (None, {
            'fields': ('job', 'applicant', 'status') 
        }),
    )

admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
