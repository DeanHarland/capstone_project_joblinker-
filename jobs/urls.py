from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Job URLs
    path('', views.JobListView.as_view(), name='job-list'),
    path('job/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    path('job/new/', views.JobCreateView.as_view(), name='job-create'),
    path('job/<int:pk>/edit/', views.JobUpdateView.as_view(), name='job-update'),
    path('job/<int:pk>/delete/', views.JobDeleteView.as_view(), name='job-delete'),
    
    # Application URLs
    path('apply/', views.ApplicationCreateView.as_view(), name='application-create'),
    path('my-applications/', views.MyApplicationsView.as_view(), name='my-applications'),
    path('application/<int:pk>/cancel/', views.ApplicationDeleteView.as_view(), name='application-cancel'),
    path('application/<int:pk>/update-status/', views.ApplicationStatusUpdateView.as_view(), name='application-status-update'),
    
    # Authentication URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    
    # Employer URLs
    path('employer/dashboard/', views.EmployerDashboardView.as_view(), name='employer-dashboard'),
]
