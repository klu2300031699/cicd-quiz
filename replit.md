# Quiz Website - Django Application

## Overview

This is a professional quiz website built with Django 5.2.7 and SQLite. The application allows users to register, take quizzes, view their results, and track their progress over time. Administrators can create and manage quizzes, add questions, and monitor user performance. The site features a responsive Bootstrap 5-based interface with support for both fixed and random question selection, timed quizzes, and comprehensive result tracking.

## User Preferences

Preferred communication style: Simple, everyday language.

## Project Structure

```
quiz_site/
├── quiz_app/                    # Main Django app
│   ├── management/
│   │   └── commands/
│   │       └── setup_initial_data.py  # Creates superuser and sample quizzes
│   ├── migrations/              # Database migrations
│   ├── static/
│   │   └── css/
│   │       └── style.css       # Custom CSS styling
│   ├── templates/
│   │   └── quiz_app/
│   │       ├── admin/          # Admin panel templates
│   │       ├── base.html       # Base template with navbar
│   │       ├── home.html       # Landing page
│   │       ├── login.html      # User login
│   │       ├── register.html   # User registration
│   │       ├── quiz_list.html  # Available quizzes
│   │       ├── take_quiz.html  # Quiz taking with timer
│   │       ├── quiz_result.html # Detailed results
│   │       └── results_history.html # User quiz history
│   ├── models.py               # Database models
│   ├── views.py                # View functions
│   ├── forms.py                # Django forms
│   ├── urls.py                 # URL routing
│   └── admin.py                # Django admin configuration
├── settings.py                 # Django settings
└── urls.py                     # Main URL configuration
```

## System Architecture

### Backend Framework
- **Django 5.2.7**: Full-stack web framework handling all backend logic, routing, and database operations
- **SQLite Database**: Lightweight relational database for storing users, quizzes, questions, and results
- **Django ORM**: Object-relational mapping for database interactions without raw SQL

### Authentication & Authorization
- **Django Built-in Auth**: Uses Django's authentication system for user registration, login, and session management
- **Login Required Decorator**: Protects quiz-related views to ensure only authenticated users can access quizzes
- **Staff/Superuser Permissions**: Admin panel restricted to staff users using `user_passes_test` decorator
- **UserProfile Model**: Extends Django's User model with additional profile information

### Data Models
The application uses four core models:

1. **UserProfile**: One-to-one relationship with Django User, tracks user metadata and quiz statistics
2. **Quiz**: Stores quiz configuration including name, description, time limits, question counts, and quiz type (fixed/random)
3. **Question**: Multiple choice questions linked to quizzes with four options and correct answer tracking
4. **UserQuizAttempt**: Records user quiz submissions with scores, answers, and timestamps using JSONField for flexible data storage

### Quiz Logic
- **Random Question Selection**: Quizzes support 'random' type where questions are shuffled using Django's `order_by('?')` 
- **Session-Based Quiz Taking**: Questions displayed on single page with form submission
- **Question ID Persistence**: Hidden form field stores question IDs to ensure consistent scoring for random quizzes
- **Timer Implementation**: JavaScript countdown timer for timed quizzes with auto-submit on expiry
- **Score Calculation**: Percentage-based scoring comparing user answers against correct answers
- **Answer Storage**: JSONField stores user selections and correct answers for detailed result review

### URL Routing
- `/` - Home page
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/quizzes/` - List available quizzes
- `/quizzes/<id>/start/` - Take specific quiz
- `/results/` - User's quiz history
- `/result/<id>/` - Detailed quiz result
- `/admin-panel/` - Admin dashboard with quiz and user management
- `/admin-panel/users/` - User management
- `/admin-panel/quizzes/` - Quiz management
- `/admin-panel/quizzes/create/` - Create new quiz
- `/admin-panel/quizzes/<id>/edit/` - Edit quiz
- `/admin-panel/results/` - View all results

### Admin Panel Features
- **User Management**: View all users with registration dates and quiz statistics
- **Quiz CRUD Operations**: Create, edit, and manage quizzes through custom forms
- **Question Management**: Add questions with formsets supporting inline editing
- **Results Dashboard**: Filter and view all user quiz attempts by user or quiz
- **Quiz Statistics**: Track total users, quizzes, and attempts

### Management Commands
- **setup_initial_data**: Custom command to create superuser and sample quiz data for initial setup
  - Creates superuser: email `Gnanesh@gmail.com`, password `Gnanesh@1561`
  - Adds "Git and Docker Basics" quiz (5 fixed questions)
  - Adds "Python Programming Fundamentals" quiz (7 questions, random selection of 5)

## External Dependencies

### Frontend Libraries
- **Bootstrap 5.3.0**: CSS framework for responsive design, loaded via CDN
- **Bootstrap JavaScript**: For interactive components (dropdowns, modals)

### Python Packages
- **Django 5.2.7**: Core web framework
- **Python Standard Library**: JSON module for JSONField operations

### Database
- **SQLite**: Default Django database, configured automatically with no external setup required
- **No Migration Dependencies**: Uses Django's built-in migration system

### Deployment Configuration
- **Development Server**: Runs on 0.0.0.0:5000 for Replit compatibility
- **Debug Mode**: Currently enabled with `DEBUG = True` and `ALLOWED_HOSTS = ['*']` (development settings)
- **Static Files**: Django's static file handling with collectstatic support

## Features Implemented

### User Features
1. ✅ User registration and authentication system
2. ✅ Home page with personalized welcome message
3. ✅ Quiz listing page with Bootstrap cards
4. ✅ Quiz taking with JavaScript countdown timer
5. ✅ Support for both fixed and random question selection
6. ✅ Automatic score calculation (percentage-based)
7. ✅ Detailed results page showing correct/incorrect answers
8. ✅ Answer explanations displayed in results
9. ✅ Quiz history tracking for each user
10. ✅ Responsive Bootstrap 5 design

### Admin Features
1. ✅ Protected admin panel (staff/superuser only)
2. ✅ Dashboard with statistics (users, quizzes, attempts)
3. ✅ User management with quiz statistics
4. ✅ Quiz creation with inline question forms
5. ✅ Quiz editing functionality
6. ✅ Results filtering by user/quiz
7. ✅ Support for random and fixed quiz types

### Security Features
- ✅ CSRF protection enabled via Django middleware
- ✅ @login_required decorators on protected views
- ✅ Password hashing using Django's authentication system
- ✅ Form validation for registration and quiz submission
- ✅ Staff-only access to admin panel

## Sample Data

Two pre-loaded quizzes:
1. **Git and Docker Basics** - 5 questions, fixed order, 15-minute timer
2. **Python Programming Fundamentals** - 7 questions (shows random 5), 20-minute timer

## Deployment Configuration

### Production Setup
The application is now configured for production deployment on Replit:

1. **Production Server**: Gunicorn WSGI server with 2 workers
2. **Static Files**: WhiteNoise middleware for efficient static file serving with compression
3. **Security Configuration**:
   - SECRET_KEY sourced from SESSION_SECRET environment variable
   - ALLOWED_HOSTS restricted to Replit domains (.repl.co, .replit.dev) and localhost
   - DEBUG defaults to False (set DEBUG=True environment variable only for development)
   - CSRF protection configured for Replit domains

### Deployment Settings
- **Deployment Type**: Autoscale (serverless deployment)
- **Run Command**: `gunicorn --bind=0.0.0.0:5000 --workers=2 quiz_site.wsgi:application`
- **Required Environment Variables**:
  - `SESSION_SECRET`: Used as Django SECRET_KEY (already available in Replit)
  - `DEBUG`: Optional, set to 'True' for development mode (defaults to False)

### Publishing the Application
To make your quiz website publicly accessible:
1. Click the "Deploy" button in the Replit interface
2. The application will be deployed using the autoscale configuration
3. You'll receive a public URL where users can access your quiz application

### Important Notes
- The SQLite database is included and will persist with your deployment
- Static files are pre-collected and will be served efficiently by WhiteNoise
- All existing user data and quizzes are preserved in db.sqlite3

## Recent Changes (October 7, 2025)

### Deployment Configuration Added
- **Production dependencies installed**: Gunicorn (WSGI server) and WhiteNoise (static file serving)
- **Security hardening**: SECRET_KEY now uses SESSION_SECRET environment variable with no insecure fallback
- **Host restrictions**: ALLOWED_HOSTS limited to Replit domains for security
- **Static file optimization**: WhiteNoise configured with compression and manifest storage
- **Deployment ready**: Autoscale deployment configuration set up for Replit publishing

### Major Feature Enhancements

#### One-Question-at-a-Time Quiz Flow
- **Complete redesign of quiz taking interface**: Questions now display one at a time instead of all at once
- **Navigation buttons**: Previous, Next, and Submit buttons for intuitive quiz navigation
- **Progress tracking**: Visual progress bar showing current question number (e.g., "Question 2 of 5")
- **Answer preservation**: All answers are saved when navigating between questions
- **Timer integration**: Countdown timer remains functional and auto-submits when time expires
- **Implementation**: JavaScript-based navigation without page reloads for smooth user experience

#### Admin User Management
- **Delete user functionality**: Admins can remove users from the system
- **Superuser protection**: Prevents accidental deletion of superuser accounts
- **Confirmation dialog**: JavaScript alert confirms deletion before proceeding
- **CSRF-protected**: Delete action uses POST request with CSRF token for security

#### Admin Results Viewing
- **Detailed results view**: New "View Details" button in admin results table
- **Question-by-question review**: Shows each question with user's answer and correct answer
- **Color-coded answers**: Green highlights for correct answers, red for incorrect
- **Visual indicators**: Badges show "User's Answer" and "Correct Answer" for clarity
- **Complete information**: Displays user info, quiz info, score, and all answer explanations

#### Profile Editing
- **User profile management**: Users can edit their first name, last name, and email
- **Form validation**: Django forms ensure data integrity
- **Navigation integration**: "Edit Profile" link in navbar when logged in

#### Dynamic Quiz Creation
- **Smart question form generation**: Question fields auto-generate based on "Total Questions Available" input
- **Data preservation**: Entered question data is preserved when changing the question count
- **Formset management**: JavaScript handles Django formsets dynamically
- **Bug fix**: Added null checks to prevent JavaScript errors on page load

### Bug Fixes
- **Fixed random quiz scoring issue**: Modified `take_quiz` view to persist question IDs in hidden form field, ensuring the same questions are graded on submission regardless of quiz type
- **Fixed JavaScript error**: Added null checks in create_quiz.html to handle missing management form elements gracefully
- **Fixed CSRF authentication**: Added Replit domains to CSRF_TRUSTED_ORIGINS for proper login/registration functionality

### Implementation Details
- **Quiz Navigation**: Uses CSS to show/hide questions, all questions remain in DOM for form submission
- **Delete User**: POST request to `/admin-panel/users/<id>/delete/` with staff permissions required
- **View Results**: GET request to `/admin-panel/results/<id>/view/` with comprehensive question analysis
- **Profile Edit**: Standard Django form handling with validation and error messages
- **Dynamic Forms**: JavaScript monitors "Total Questions Available" input and regenerates formsets accordingly

## How to Use

### For Users
1. Register a new account or login
2. Browse available quizzes on the Quizzes page
3. Click "Start Quiz" to begin
4. Answer all questions before time expires
5. Submit to see results with detailed answer review
6. View quiz history in Results page

### For Admins
1. Login with admin credentials (Gnanesh@gmail.com / Gnanesh@1561)
2. Access Admin Panel from the navbar
3. Create new quizzes with questions
4. Monitor user activity and results
5. Edit existing quizzes as needed

## Technical Notes

- **Random Quiz Fix**: Question IDs are now persisted in the form to prevent regeneration on POST, ensuring accurate scoring
- **Timer Auto-Submit**: JavaScript timer automatically submits the quiz when time expires
- **Bootstrap 5**: All templates use Bootstrap 5 components for professional appearance
- **Responsive Design**: Mobile-friendly layout with responsive navbar and cards
- **Production Ready**: Ready for deployment with proper CSRF protection and authentication
