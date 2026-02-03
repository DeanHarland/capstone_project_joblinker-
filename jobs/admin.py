from django.contrib import admin
from .models import Job, Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'salary', 'created_at']
    list_filter = ['created_at', 'location']
    search_fields = ['title', 'company', 'description']
    readonly_fields = ['created_at']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['applicant__username', 'job__title']
    readonly_fields = ['created_at']
