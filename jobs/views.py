from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Job, Application, Profile
from .forms import JobForm, ApplicationForm, CustomUserCreationForm


class CustomLoginView(DjangoLoginView):
    template_name = 'auth/login.html'
    
    def get_success_url(self):
        """Redirect based on user role"""
        user = self.request.user
        try:
            profile = Profile.objects.get(user=user)
            if profile.role == 'employer':
                return reverse_lazy('employer-dashboard')
            else:
                return reverse_lazy('job-list')
        except Profile.DoesNotExist:
            return reverse_lazy('job-list')


class CustomLogoutView(DjangoLogoutView):
    next_page = reverse_lazy('job-list')
    http_method_names = ['get', 'post', 'options']


class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Add search functionality if search query exists
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                title__icontains=search_query
            ) | queryset.filter(
                company__icontains=search_query
            ) | queryset.filter(
                location__icontains=search_query
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get user's applied jobs if authenticated
        if self.request.user.is_authenticated:
            applied_job_ids = Application.objects.filter(
                applicant=self.request.user
            ).values_list('job_id', flat=True)
            context['applied_job_ids'] = set(applied_job_ids)
        else:
            context['applied_job_ids'] = set()
        return context


class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if user has already applied to this job
        if self.request.user.is_authenticated:
            context['has_applied'] = Application.objects.filter(
                job=self.object,
                applicant=self.request.user
            ).exists()
        return context


class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('job-list')
    login_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Job'
        return context

    def test_func(self):
        return self.request.user.profile.role == 'employer'

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Job created successfully!')
        return response


class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('job-list')
    login_url = reverse_lazy('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Job'
        return context

    def test_func(self):
        return (
            self.request.user.profile.role == 'employer'
            and self.get_object().posted_by == self.request.user
        )
    
    def form_valid(self, form):
        messages.success(self.request, 'Job updated successfully!')
        return super().form_valid(form)


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'jobs/job_confirm_delete.html'
    success_url = reverse_lazy('job-list')
    login_url = reverse_lazy('login')
    context_object_name = 'job'

    def test_func(self):
        return (
            self.request.user.profile.role == 'employer'
            and self.get_object().posted_by == self.request.user
        )
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Job deleted successfully!')
        return super().delete(request, *args, **kwargs)


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'jobs/application_form.html'
    login_url = reverse_lazy('login')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        job_id = self.request.POST.get('job_id')
        if job_id:
            initial['job'] = Job.objects.get(pk=job_id)
        return initial
    
    def form_valid(self, form):
        form.instance.applicant = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Application submitted successfully!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('job-detail', kwargs={'pk': self.object.job.pk})


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response


class EmployerDashboardView(LoginRequiredMixin, View):
    """Dashboard for employers to manage their job postings"""
    login_url = reverse_lazy('login')
    
    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            if profile.role != 'employer':
                messages.error(request, 'Only employers can access this page.')
                return redirect('job-list')
        except Profile.DoesNotExist:
            messages.error(request, 'Profile not found.')
            return redirect('job-list')
        
        # Get all jobs posted by this employer
        jobs = Job.objects.filter(posted_by=request.user)
        
        context = {
            'jobs': jobs,
            'total_jobs': jobs.count(),
            'total_applications': Application.objects.filter(job__posted_by=request.user).count(),
        }
        return render(request, 'jobs/employer_dashboard.html', context)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get IDs of jobs the user has applied to
        if self.request.user.is_authenticated:
            applied_job_ids = Application.objects.filter(
                applicant=self.request.user
            ).values_list('job_id', flat=True)
            context['applied_job_ids'] = set(applied_job_ids)
        else:
            context['applied_job_ids'] = set()
        return context

