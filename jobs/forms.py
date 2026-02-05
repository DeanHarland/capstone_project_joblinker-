from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Job, Application, Profile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        widget=forms.RadioSelect,
        label='Select your role'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['role'].widget.attrs.update({'class': 'form-check-input'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create profile with selected role
            Profile.objects.create(user=user, role=self.cleaned_data['role'])
        return user


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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your cover letter here...',
                'rows': 8,
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx',
            }),
        }
        labels = {
            'cover_letter': 'Cover Letter',
            'resume': 'Resume (PDF, DOC, or DOCX)',
        }
    
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            # Check file size (max 5MB)
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Resume file size must not exceed 5MB.")
            # Check file extension
            allowed_extensions = ['pdf', 'doc', 'docx']
            file_extension = resume.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise forms.ValidationError("Only PDF, DOC, and DOCX files are allowed.")
        return resume