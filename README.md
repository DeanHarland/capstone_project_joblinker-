# JobLinker – AI-Augmented Full-Stack Django Application

Live site: https://joblinker-32ea19931b20.herokuapp.com/  
Repository: https://github.com/DeanHarland/capstone_project_joblinker-

---

## Project Overview

**JobLinker** is a full-stack web application built using the Django framework that connects **employers** with **job seekers**. Employers can create and manage job listings, while job seekers can browse jobs, submit applications, and manage their own applications.

The project was developed as an individual **Full-Stack Capstone Project** for the **Code Institute AI-Augmented Full-Stack Bootcamp**, demonstrating competency across UX design, backend development, authentication, testing, deployment, version control, and the strategic use of AI tools.

---

## Project Purpose

- Provide a clear, role-based job board platform
- Demonstrate secure, scalable full-stack development with Django
- Apply Agile methodology and best practices
- Showcase AI-assisted development in a real-world workflow

---

## User Roles

| Role | Permissions |
|-----|------------|
| Admin | Full system access via Django Admin |
| Employer | Create, edit, delete job listings; review applications |
| Job Seeker | View jobs, apply for jobs, cancel applications |

---

## Features

### Front-End
- Responsive design using Bootstrap
- Accessible navigation and semantic HTML
- Clear user feedback via notifications
- Conditional UI rendering based on login state and role

### Back-End
- Custom Django models for jobs and applications
- Full CRUD functionality
- Role-based access control
- PostgreSQL database integration
- Secure environment variable management

---

## User Stories (Summary)

### Employer
- As an employer, I want to create job listings so that candidates can apply
- As an employer, I want to edit or delete job listings I own
- As an employer, I want to review applications for my job postings

### Job Seeker
- As a job seeker, I want to browse available jobs
- As a job seeker, I want to apply for jobs
- As a job seeker, I want to cancel my application if I change my mind

### General User
- As a user, I want to register and log in securely
- As a user, I want to see feedback when I perform actions

All user stories were tracked using a **GitHub Project Board**:  
https://github.com/users/DeanHarland/projects/10

---

## UX Design, Accessibility & Responsiveness (LO1)

### UX Process
The UX design evolved iteratively during development. Layouts and navigation were refined as features were added and tested, prioritising clarity and ease of use for different user roles.

### Accessibility
- Semantic HTML elements used throughout
- Clear labels and validation messages in forms
- Colour contrast and readable typography via Bootstrap
- Keyboard-accessible navigation

### Responsiveness
- Mobile-first responsive layout
- Bootstrap grid system and utility classes
- Fully functional across mobile, tablet, and desktop viewports

---

## Agile Development (LO1.3)

- Agile methodology using GitHub Projects
- User stories created and tracked
- Tasks moved across **To Do → In Progress → Done**
- Incremental development with regular commits

---

## Data Model & Object-Oriented Design (LO2, LO7)

### Custom Models

**Job**
- title
- company
- location
- description
- salary
- created_by (ForeignKey → User)

**Application**
- job (ForeignKey → Job)
- applicant (ForeignKey → User)
- status
- applied_at

### Relationships
- One employer → many jobs
- One job → many applications
- One job seeker → many applications

Django’s ORM was used to implement object-oriented design principles and manage database relationships.

---

## CRUD Functionality (LO2.2)

| Feature | Create | Read | Update | Delete |
|-------|--------|------|--------|--------|
| Jobs | ✅ | ✅ | ✅ | ✅ |
| Applications | ✅ | ✅ | ❌ | ✅ |

CRUD actions are restricted by user role to ensure data integrity and security.

---

## Forms, Validation & Notifications (LO2)

- Django ModelForms used throughout
- Server-side validation enforced
- Clear error and success messages displayed using Django messages framework
- Forms designed for accessibility and usability

---

## Authentication & Authorization (LO3)

### Authentication
- User registration and login using Django’s authentication system
- Secure password handling
- Logout functionality

### Authorization
- Employers can only manage their own job listings
- Job seekers can only manage their own applications
- Unauthorized actions are blocked and redirected

Navigation and UI elements dynamically reflect authentication state.

---

## Testing (LO4)

### Manual Testing
Manual testing covered:
- CRUD operations
- Authentication and authorization
- Role-based restrictions
- Responsive layout
- User feedback and notifications

### Automated Testing
Django unit tests were implemented to test:
- Model creation
- CRUD operations
- Access control
- Form validation

Tests were run using:
```bash
python manage.py test
```

### JavaScript Testing (LO4.2)

Minimal custom JavaScript was used in this project. Bootstrap JavaScript components were utilised for UI behaviour. As no custom JavaScript logic was implemented, no separate JavaScript test suite was required.

---

## Version Control & Secure Code Management (LO5)

### Git & GitHub Usage
- Git used consistently throughout development
- Clear, descriptive commit messages aligned with features and fixes
- Logical commit frequency reflecting incremental progress
- Full development history visible in the GitHub repository

### Secure Code Management
- `.gitignore` used to prevent sensitive files from being committed
- All secret keys and credentials managed via environment variables
- No passwords, tokens, or API keys stored in the repository

---

## Deployment (LO6)

### Hosting
- Application deployed on **Heroku**
- **PostgreSQL database** provided by Code Institute

### Deployment Steps
1. Configure environment variables on Heroku
2. Set `DEBUG=False`
3. Configure `ALLOWED_HOSTS`
4. Add `Procfile` and `runtime.txt`
5. Push code to Heroku
6. Run database migrations
7. Collect static files

### Security
- No sensitive data committed to the repository
- Environment variables used for all secret keys and configurations
- Production settings correctly configured

---

## AI-Assisted Development (LO8)

### Tools Used
- ChatGPT
- GitHub Copilot

### AI Usage
AI tools were used throughout the development process to:
- Plan project structure and Agile workflow
- Generate boilerplate Django code
- Debug configuration, logic, and deployment issues
- Improve code clarity, performance, and structure
- Assist with creating automated tests
- Optimise development efficiency

All AI-generated output was reviewed, adapted, and fully understood by the developer before inclusion.

---

## Technologies Used

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

## Future Improvements

- Job filtering and search functionality for job seekers
- Email notifications for job applications and status changes
- Pagination for large job listings
- Enhanced user profile features

---

## Acknowledgements

This project was completed as part of the **Code Institute AI-Augmented Full-Stack Bootcamp** and demonstrates the integration of modern full-stack development practices with AI-assisted workflows.
