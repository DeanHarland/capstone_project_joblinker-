from django import forms
from .models import Job, Application


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'company', 'location', 'salary']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job title',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job description',
                'rows': 5,
                'required': True,
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name',
                'required': True,
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter location',
                'required': True,
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter salary (optional)',
                'step': '0.01',
            }),
        }
        labels = {
            'title': 'Job Title',
            'description': 'Job Description',
            'company': 'Company Name',
            'location': 'Location',
            'salary': 'Salary',
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) < 3:
            raise forms.ValidationError("Job title must be at least 3 characters long.")
        return title
    
    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary is not None and salary < 0:
            raise forms.ValidationError("Salary cannot be negative.")
        return salary


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['job']
        widgets = {
            'job': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
        }
        labels = {
            'job': 'Select Job',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter out jobs the user has already applied to
        if user:
            applied_job_ids = Application.objects.filter(applicant=user).values_list('job_id', flat=True)
            self.fields['job'].queryset = Job.objects.exclude(id__in=applied_job_ids)


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
        }
        labels = {
            'status': 'Application Status',
        }
