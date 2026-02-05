from django.contrib import admin
from .models import Job, Application, Profile, Notification


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin interface for user profiles."""
    
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username']
    readonly_fields = ['user']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Profile Details', {
            'fields': ('role',)
        }),
    )


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """Admin interface for job postings."""
    
    list_display = ['title', 'company', 'location', 'salary', 'posted_by', 'created_at']
    list_filter = ['created_at', 'location', 'posted_by']
    search_fields = ['title', 'company', 'description']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Job Information', {
            'fields': ('title', 'company', 'posted_by')
        }),
        ('Details', {
            'fields': ('description', 'location', 'salary')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Admin interface for job applications."""
    
    list_display = ['applicant', 'job', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['applicant__username', 'job__title']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Application Details', {
            'fields': ('job', 'applicant')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for notifications."""
    
    list_display = ['employer', 'get_applicant', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['employer__username', 'application__applicant__username']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Notification Information', {
            'fields': ('employer', 'application')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_applicant(self, obj):
        """Display applicant username for easier viewing."""
        return obj.application.applicant.username
    get_applicant.short_description = 'Applicant'
