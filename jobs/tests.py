from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Job, Application, Profile
from .forms import JobForm, ApplicationForm, CustomUserCreationForm


class JobModelTestCase(TestCase):
    """Test cases for Job model"""
    
    def setUp(self):
        """Create test data"""
        self.employer = User.objects.create_user(
            username='employer',
            email='employer@test.com',
            password='testpass123'
        )
        Profile.objects.create(user=self.employer, role='employer')
        
        self.job = Job.objects.create(
            title='Software Engineer',
            description='Build amazing software',
            company='Tech Corp',
            location='San Francisco, CA',
            salary=150000.00,
            posted_by=self.employer
        )
    
    def test_job_creation(self):
        """Test that job is created successfully"""
        self.assertEqual(self.job.title, 'Software Engineer')
        self.assertEqual(self.job.company, 'Tech Corp')
        self.assertEqual(self.job.posted_by, self.employer)
    
    def test_job_string_representation(self):
        """Test job __str__ method"""
        expected_str = f"Software Engineer at Tech Corp"
        self.assertEqual(str(self.job), expected_str)
    
    def test_job_ordering(self):
        """Test jobs are ordered by creation date (newest first)"""
        job2 = Job.objects.create(
            title='Product Manager',
            description='Manage products',
            company='Tech Corp',
            location='NYC',
            posted_by=self.employer
        )
        # Ensure job2 has a later created_at timestamp
        Job.objects.filter(pk=job2.pk).update(created_at=timezone.now())
        jobs = Job.objects.all()
        self.assertEqual(jobs[0], job2)  # Newest first
        self.assertEqual(jobs[1], self.job)  # Oldest second


class ApplicationModelTestCase(TestCase):
    """Test cases for Application model"""
    
    def setUp(self):
        """Create test data"""
        # Create employer
        self.employer = User.objects.create_user(
            username='employer',
            email='employer@test.com',
            password='testpass123'
        )
        Profile.objects.create(user=self.employer, role='employer')
        
        # Create job seeker
        self.job_seeker = User.objects.create_user(
            username='jobseeker',
            email='seeker@test.com',
            password='testpass123'
        )
        Profile.objects.create(user=self.job_seeker, role='jobseeker')
        
        # Create job
        self.job = Job.objects.create(
            title='Software Engineer',
            description='Build software',
            company='Tech Corp',
            location='SF',
            posted_by=self.employer
        )
        
        # Create application
        self.application = Application.objects.create(
            job=self.job,
            applicant=self.job_seeker,
            status='pending'
        )
    
    def test_application_creation(self):
        """Test application is created successfully"""
        self.assertEqual(self.application.job, self.job)
        self.assertEqual(self.application.applicant, self.job_seeker)
        self.assertEqual(self.application.status, 'pending')
    
    def test_application_string_representation(self):
        """Test application __str__ method"""
        expected_str = "jobseeker - Software Engineer (pending)"
        self.assertEqual(str(self.application), expected_str)
    
    def test_unique_together_constraint(self):
        """Test that duplicate applications are not allowed"""
        with self.assertRaises(Exception):
            Application.objects.create(
                job=self.job,
                applicant=self.job_seeker,
                status='pending'
            )
    
    def test_application_status_choices(self):
        """Test application status can be changed"""
        self.application.status = 'reviewed'
        self.application.save()
        self.assertEqual(self.application.status, 'reviewed')
        
        self.application.status = 'accepted'
        self.application.save()
        self.assertEqual(self.application.status, 'accepted')


class JobFormTestCase(TestCase):
    """Test cases for JobForm"""
    
    def test_valid_job_form(self):
        """Test form with valid data"""
        form_data = {
            'title': 'Data Scientist',
            'description': 'Work with machine learning',
            'company': 'AI Corp',
            'location': 'Boston, MA',
            'salary': '120000.00'
        }
        form = JobForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_job_form_missing_required_field(self):
        """Test form with missing required fields"""
        form_data = {
            'title': 'Data Scientist',
            'description': '',  # Missing required field
            'company': 'AI Corp',
            'location': 'Boston'
        }
        form = JobForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)
    
    def test_job_form_title_too_short(self):
        """Test form with title less than 3 characters"""
        form_data = {
            'title': 'QA',  # Too short
            'description': 'Work in QA',
            'company': 'Tech Corp',
            'location': 'NYC',
        }
        form = JobForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_job_form_negative_salary(self):
        """Test form with negative salary"""
        form_data = {
            'title': 'Developer',
            'description': 'Build apps',
            'company': 'Tech Corp',
            'location': 'NYC',
            'salary': '-50000.00'
        }
        form = JobForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('salary', form.errors)
    
    def test_job_form_optional_salary(self):
        """Test form with empty salary (optional field)"""
        form_data = {
            'title': 'Developer',
            'description': 'Build apps',
            'company': 'Tech Corp',
            'location': 'NYC',
            'salary': ''
        }
        form = JobForm(data=form_data)
        self.assertTrue(form.is_valid())


class ApplicationFormTestCase(TestCase):
    """Test cases for ApplicationForm"""
    
    def setUp(self):
        """Create test data"""
        self.employer = User.objects.create_user(
            username='employer',
            email='employer@test.com',
            password='testpass123'
        )
        Profile.objects.create(user=self.employer, role='employer')
        
        self.job_seeker = User.objects.create_user(
            username='jobseeker',
            email='seeker@test.com',
            password='testpass123'
        )
        Profile.objects.create(user=self.job_seeker, role='jobseeker')
        
        self.job1 = Job.objects.create(
            title='Job 1',
            description='Test',
            company='Corp',
            location='SF',
            posted_by=self.employer
        )
        
        self.job2 = Job.objects.create(
            title='Job 2',
            description='Test',
            company='Corp',
            location='NYC',
            posted_by=self.employer
        )
    
    def test_application_form_valid(self):
        """Test form with valid job selection"""
        form_data = {'job': self.job1.id}
        form = ApplicationForm(data=form_data, user=self.job_seeker)
        self.assertTrue(form.is_valid())
    
    def test_application_form_filters_applied_jobs(self):
        """Test that already applied jobs are filtered out"""
        # Apply to job1
        Application.objects.create(
            job=self.job1,
            applicant=self.job_seeker,
            status='pending'
        )
        
        # Form should only show job2
        form = ApplicationForm(user=self.job_seeker)
        available_jobs = form.fields['job'].queryset
        self.assertEqual(available_jobs.count(), 1)
        self.assertEqual(available_jobs[0], self.job2)

    def test_application_form_requires_job(self):
        """Test form requires job selection"""
        form = ApplicationForm(data={}, user=self.job_seeker)
        self.assertFalse(form.is_valid())
        self.assertIn('job', form.errors)

    def test_application_form_without_user_shows_all_jobs(self):
        """Test form without user shows all jobs"""
        form = ApplicationForm()
        available_jobs = list(form.fields['job'].queryset)
        self.assertEqual(set(available_jobs), {self.job1, self.job2})


class JobCRUDViewsTestCase(TestCase):
    """Test cases for Job CRUD views"""
    
    def setUp(self):
        """Create test data"""
        self.client = Client()
        
        # Create employer
        self.employer = User.objects.create_user(
            username='employer',
            email='employer@test.com',
            password='testpass123'
        )
        Profile.objects.create(user=self.employer, role='employer')

        # Create another employer
        self.other_employer = User.objects.create_user(
            username='employer2',
            email='employer2@test.com',
            password='testpass123'
        )
        Profile.objects.create(user=self.other_employer, role='employer')
        
        # Create job seeker
        self.job_seeker = User.objects.create_user(
            username='jobseeker',
            email='seeker@test.com',
            password='testpass123'
        )
        Profile.objects.create(user=self.job_seeker, role='jobseeker')
        
        # Create a job
        self.job = Job.objects.create(
            title='Software Engineer',
            description='Build software',
            company='Tech Corp',
            location='SF',
            posted_by=self.employer
        )
    
    def test_job_list_view(self):
        """Test job list view is accessible"""
        response = self.client.get(reverse('job-list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.job, response.context['jobs'])
    
    def test_job_detail_view(self):
        """Test job detail view"""
        response = self.client.get(reverse('job-detail', args=[self.job.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['job'], self.job)
    
    def test_job_create_requires_login(self):
        """Test job create view requires authentication"""
        response = self.client.get(reverse('job-create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue('/login/' in response.url)
    
    def test_job_create_requires_employer_role(self):
        """Test job create requires employer role"""
        self.client.login(username='jobseeker', password='testpass123')
        response = self.client.get(reverse('job-create'))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_job_update_requires_login(self):
        """Test job update requires authentication"""
        response = self.client.get(reverse('job-update', args=[self.job.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue('/login/' in response.url)

    def test_job_delete_requires_login(self):
        """Test job delete requires authentication"""
        response = self.client.get(reverse('job-delete', args=[self.job.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue('/login/' in response.url)

    def test_job_update_requires_employer_role(self):
        """Test job update requires employer role"""
        self.client.login(username='jobseeker', password='testpass123')
        response = self.client.get(reverse('job-update', args=[self.job.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_job_delete_requires_employer_role(self):
        """Test job delete requires employer role"""
        self.client.login(username='jobseeker', password='testpass123')
        response = self.client.get(reverse('job-delete', args=[self.job.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_job_update_requires_owner(self):
        """Test job update requires job owner"""
        self.client.login(username='employer2', password='testpass123')
        response = self.client.get(reverse('job-update', args=[self.job.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_job_delete_requires_owner(self):
        """Test job delete requires job owner"""
        self.client.login(username='employer2', password='testpass123')
        response = self.client.get(reverse('job-delete', args=[self.job.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden
    
    def test_job_create_as_employer(self):
        """Test employer can create job"""
        self.client.login(username='employer', password='testpass123')
        job_data = {
            'title': 'New Job',
            'description': 'New job description',
            'company': 'New Corp',
            'location': 'Boston',
            'salary': '100000.00'
        }
        response = self.client.post(reverse('job-create'), job_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Verify job was created
        new_job = Job.objects.get(title='New Job')
        self.assertEqual(new_job.posted_by, self.employer)
        self.assertEqual(new_job.company, 'New Corp')
    
    def test_job_update(self):
        """Test job update"""
        self.client.login(username='employer', password='testpass123')
        update_data = {
            'title': 'Updated Title',
            'description': self.job.description,
            'company': self.job.company,
            'location': 'NYC',
            'salary': '200000.00'
        }
        response = self.client.post(
            reverse('job-update', args=[self.job.id]),
            update_data
        )
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Verify job was updated
        updated_job = Job.objects.get(id=self.job.id)
        self.assertEqual(updated_job.title, 'Updated Title')
        self.assertEqual(updated_job.location, 'NYC')
    
    def test_job_delete(self):
        """Test job deletion"""
        self.client.login(username='employer', password='testpass123')
        job_id = self.job.id
        
        response = self.client.post(reverse('job-delete', args=[job_id]))
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Verify job was deleted
        self.assertFalse(Job.objects.filter(id=job_id).exists())


class ApplicationViewTestCase(TestCase):
    """Test cases for Application views"""
    
    def setUp(self):
        """Create test data"""
        self.client = Client()
        
        # Create employer
        self.employer = User.objects.create_user(
            username='employer',
            email='employer@test.com',
            password='testpass123'
        )
        Profile.objects.create(user=self.employer, role='employer')
        
        # Create job seeker
        self.job_seeker = User.objects.create_user(
            username='jobseeker',
            email='seeker@test.com',
            password='testpass123'
        )
        Profile.objects.create(user=self.job_seeker, role='jobseeker')
        
        # Create job
        self.job = Job.objects.create(
            title='Software Engineer',
            description='Build software',
            company='Tech Corp',
            location='SF',
            posted_by=self.employer
        )
    
    def test_application_create_requires_login(self):
        """Test application requires authentication"""
        response = self.client.get(reverse('application-create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_job_seeker_can_apply(self):
        """Test job seeker can submit application"""
        self.client.login(username='jobseeker', password='testpass123')
        app_data = {'job': self.job.id}
        
        response = self.client.post(reverse('application-create'), app_data)
        self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Verify application was created
        application = Application.objects.get(
            job=self.job,
            applicant=self.job_seeker
        )
        self.assertEqual(application.status, 'pending')
    
    def test_duplicate_application_not_allowed(self):
        """Test that duplicate applications are rejected"""
        # First application
        Application.objects.create(
            job=self.job,
            applicant=self.job_seeker,
            status='pending'
        )
        
        # Try to apply again
        self.client.login(username='jobseeker', password='testpass123')
        app_data = {'job': self.job.id}
        
        # Should fail due to unique_together constraint
        response = self.client.post(reverse('application-create'), app_data)
        # Should not create duplicate - only 1 application should exist
        self.assertEqual(Application.objects.filter(
            job=self.job,
            applicant=self.job_seeker
        ).count(), 1)


class AuthenticationTestCase(TestCase):
    """Test cases for authentication and role-based access"""
    
    def setUp(self):
        """Create test data"""
        self.client = Client()
    
    def test_user_registration(self):
        """Test user can register with role"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'role': 'employer'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Profile.objects.filter(user=user, role='employer').exists())
    
    def test_duplicate_email_not_allowed(self):
        """Test that duplicate emails are rejected"""
        User.objects.create_user(
            username='user1',
            email='test@test.com',
            password='pass123'
        )
        
        form_data = {
            'username': 'user2',
            'email': 'test@test.com',  # Duplicate
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'role': 'jobseeker'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

