from django.contrib import admin
from .models import Commission, Job, JobApplication

class JobInline(admin.TabularInline):  # Using TabularInline for Jobs under Commission
    model = Job
    extra = 1  
    fields = ('role', 'manpower_required', 'status')  # Display these fields in the inline form
    list_filter = ('status',)  # Filter status in the inline

class JobApplicationInline(admin.TabularInline):  # Using TabularInline for JobApplications under Job
    model = JobApplication
    extra = 1  
    fields = ('applicant', 'status', 'applied_on')  # Display these fields in the inline form
    list_filter = ('status',)  # Filter status in the inline

class CommissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'author', 'created_on', 'updated_on')
    search_fields = ('title', 'author__display_name')
    list_filter = ('status', 'created_on')
    inlines = [JobInline]  # Add JobInline for managing jobs within a commission

    # Add a dropdown for status field in the admin form
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'author', 'status')  # Including status field here
        }),
    )

class JobAdmin(admin.ModelAdmin):
    list_display = ('commission', 'role', 'manpower_required', 'status')
    search_fields = ('role', 'commission__title')
    list_filter = ('status',)
    inlines = [JobApplicationInline]  # Add JobApplicationInline for managing applications within a job

    # Add a dropdown for status field in the admin form
    fieldsets = (
        (None, {
            'fields': ('commission', 'role', 'manpower_required', 'status')  # Including status field here
        }),
    )

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_on')
    search_fields = ('job__role', 'applicant__display_name')
    list_filter = ('status',)

    # Add a dropdown for status field in the admin form
    fieldsets = (
        (None, {
            'fields': ('job', 'applicant', 'status')  # Including status field here
        }),
    )

# Register models with the admin site
admin.site.register(Commission, CommissionAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
