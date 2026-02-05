from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Application, Notification


@receiver(post_save, sender=Application)
def create_notification_on_application(sender, instance, created, **kwargs):
    """
    Signal handler that creates a notification and sends an email
    when a new application is submitted.
    """
    if created:
        # Create notification record
        employer = instance.job.posted_by
        notification = Notification.objects.create(
            employer=employer,
            application=instance,
            is_read=False
        )
        
        # Send email notification to employer
        send_application_notification_email(instance, employer)


def send_application_notification_email(application, employer):
    """
    Send email notification to employer about new application.
    """
    try:
        subject = f"New Application: {application.job.title}"
        
        message = f"""
Hello {employer.first_name or employer.username},

A new applicant has applied for your job posting:

Job Title: {application.job.title}
Company: {application.job.company}
Applicant: {application.applicant.first_name} {application.applicant.last_name}
Applied on: {application.created_at.strftime('%B %d, %Y at %I:%M %p')}

Visit your dashboard to review the application:
{settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'https://joblinker.example.com'}/employer-dashboard/

Best regards,
JobLinker Team
        """
        
        # Send email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL or 'noreply@joblinker.com',
            [employer.email],
            fail_silently=True,  # Don't fail if email fails
        )
    except Exception as e:
        # Log the error but don't break the application flow
        print(f"Error sending notification email: {str(e)}")
