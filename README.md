# JobLinker – AI-Augmented Full-Stack Django Application

**Live Site:** https://joblinker-32ea19931b20.herokuapp.com/  
**Repository:** https://github.com/DeanHarland/capstone_project_joblinker-

---

# Project Overview

JobLinker is a full-stack web application built with Django that connects employers and job seekers through a role-based job board platform.

Employers can create and manage job listings, while job seekers can browse listings, submit applications, and manage their applications securely.

This project was developed as an individual Full-Stack Capstone Project for the Code Institute AI-Augmented Full-Stack Bootcamp. It demonstrates competency in:

- UX design and accessibility
- Full-stack Django development
- Role-based authentication and authorization
- Database modelling and CRUD operations
- Testing (manual and automated)
- Secure deployment
- Version control best practices
- Strategic AI-assisted development

---

# Project Purpose

The purpose of JobLinker is to:

- Provide a secure, role-based job board platform
- Demonstrate scalable, production-ready Django development
- Apply Agile methodology in a real-world project
- Integrate AI tools effectively into a professional development workflow

---

# User Roles & Permissions

| Role | Permissions |
|------|-------------|
| Admin | Full access via Django Admin |
| Employer | Create, edit, delete job listings; review applications |
| Job Seeker | View jobs, apply for jobs, cancel applications |

Access control is enforced both at the view level and within templates to ensure data integrity and security.

---

# UX Design Process (LO1)

## Strategy

Target users:
- Employers seeking to advertise positions
- Job seekers searching and applying for roles

Primary goals:
- Clear navigation
- Simple, intuitive workflows
- Strong separation of user roles
- Secure interaction with data

---

## Scope

Core features were prioritised using user stories:

### Employer
- Create job listings
- Edit/delete own listings
- View applications

### Job Seeker
- Browse job listings
- Apply for jobs
- Cancel applications

### General User
- Register and log in securely
- Receive feedback on actions

All user stories were tracked using GitHub Projects and progressed through To Do → In Progress → Done.

---

## Structure

The information architecture separates:

- Public job listings
- Employer dashboard
- Job seeker dashboard
- Authentication pages

Navigation adapts dynamically based on login state and user role.

---

## Skeleton (Wireframes)

Wireframes were created during initial planning and refined iteratively throughout development. Layout decisions prioritised:

- Clear hierarchy of information
- Prominent action buttons
- Minimal cognitive load
- Distinct dashboards per role

---

## Surface (Visual Design)

- Bootstrap grid system used for responsive design
- Clean typography and spacing for readability
- Consistent UI components across the application
- Clear visual feedback using alerts and success messages

---

# Accessibility (LO1.1)

Accessibility was considered throughout development:

- Semantic HTML elements used consistently
- All forms include associated labels
- Server-side validation ensures meaningful error messages
- Colour contrast handled using Bootstrap standards
- Keyboard-accessible navigation
- Responsive design tested across mobile, tablet, and desktop devices

No major accessibility issues were identified during testing.

---

# Features

## Front-End

- Responsive Bootstrap design
- Conditional UI rendering based on user role
- Django messages framework for user feedback
- Clean and consistent layout across devices

## Back-End

- Custom Django models
- Full CRUD functionality
- Role-based access control
- PostgreSQL database integration
- Secure environment variable configuration

---

# Data Model & Object-Oriented Design (LO2 & LO7)

## Custom Models

### Job
- title
- company
- location
- description
- salary
- created_by (ForeignKey → User)

### Application
- job (ForeignKey → Job)
- applicant (ForeignKey → User)
- status
- applied_at

## Relationships

- One employer → Many jobs
- One job → Many applications
- One job seeker → Many applications

Django’s ORM was used to implement object-oriented principles and manage all database relationships securely.

---

# CRUD Functionality (LO2.2)

| Feature | Create | Read | Update | Delete |
|----------|--------|------|--------|--------|
| Jobs | ✅ | ✅ | ✅ | ✅ |
| Applications | ✅ | ✅ | ❌ | ✅ |

CRUD actions are restricted by user role to prevent unauthorised data manipulation.

---

# Forms, Validation & Notifications (LO2.4)

- Django ModelForms implemented for all data entry
- Server-side validation ensures secure input handling
- Clear error and success messages via Django messages framework
- Forms designed for clarity and accessibility

---

# Authentication & Authorization (LO3)

## Authentication

- Django’s built-in authentication system used
- Secure password hashing
- Login, registration, and logout functionality implemented

## Authorization

- `@login_required` decorators protect restricted views
- Ownership checks ensure users can only modify their own records
- Template logic conditionally renders content based on user role
- Unauthorised access redirects users appropriately

Login state is reflected dynamically in navigation and dashboards.

---

# Testing (LO4)

## Automated Testing

Django unit tests were implemented to cover:

- Model creation
- CRUD functionality
- Access control restrictions
- Form validation

Tests were executed using:

```
python manage.py test
```

All core functionality passed automated tests.

---

## Manual Testing

Manual testing covered:

- Registration & login
- Role-based access restrictions
- CRUD functionality
- Notification messages
- Responsive design across device sizes

| Feature | Expected Result | Status |
|----------|----------------|--------|
| Employer creates job | Job saved and displayed | Pass |
| Job seeker applies | Application recorded | Pass |
| Unauthorized edit attempt | Access denied | Pass |

---

## JavaScript Testing

Minimal custom JavaScript was used. Bootstrap components provide UI behaviour. As no custom JS logic was implemented, separate JS testing was not required.

---

# Version Control & Secure Code Management (LO5)

## Git Usage

- Regular, incremental commits
- Clear, descriptive commit messages
- Commit history reflects feature development and bug fixes
- GitHub Project Board used for tracking progress

## Security

- `.gitignore` prevents sensitive files from being committed
- All secrets managed via environment variables
- No passwords or API keys stored in repository

---

# Deployment (LO6)

## Hosting

- Application deployed on Heroku
- PostgreSQL database configured for production

## Deployment Process

1. Configure environment variables
2. Set `DEBUG=False`
3. Configure `ALLOWED_HOSTS`
4. Add `Procfile` and runtime configuration
5. Run migrations
6. Collect static files

The deployed version matches local development functionality.

---

## Production Security

- DEBUG disabled
- Secret keys stored securely
- No sensitive data exposed in repository
- Secure database configuration

---

# AI-Assisted Development (LO8)

## Tools Used

- ChatGPT
- GitHub Copilot

## AI Contributions

### Planning
AI assisted with project structure planning and workflow design.

### Code Generation
AI supported generation of boilerplate Django views, forms, and logic.

### Debugging
AI helped diagnose configuration issues, deployment errors, and logic bugs.

### Testing
GitHub Copilot assisted in generating unit tests, which were reviewed and refined manually.

### Optimisation
AI suggestions improved code clarity and development efficiency.

All AI-generated content was reviewed, adapted, and fully understood before integration.

---

# Technologies Used

- Python
- Django
- PostgreSQL
- HTML5
- CSS3
- Bootstrap
- Git & GitHub
- Heroku
- ChatGPT
- GitHub Copilot

---

# Future Improvements

- Job filtering and search functionality
- Pagination for large job listings
- Email notifications for application updates
- Application status updates by employers
- Enhanced user profile features

---

# Known Limitations

- Employers cannot currently update application status
- No advanced job filtering implemented yet

---

# Acknowledgements

This project was completed as part of the Code Institute AI-Augmented Full-Stack Bootcamp.

It demonstrates full-stack development competency combined with structured AI-assisted workflow integration.

---

# Final Statement

JobLinker satisfies all required Learning Outcomes for the Full-Stack Capstone Project, demonstrating:

- Professional UX design
- Secure role-based authentication
- Structured database modelling
- Full CRUD implementation
- Testing and validation
- Secure deployment practices
- Strategic AI integration
