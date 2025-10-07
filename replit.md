# Quiz Website - Django Application

## Overview
This project is a professional quiz website built with Django 5.2.7 and SQLite. It enables users to register, participate in quizzes, track their progress, and review results. Administrators have full control over quiz creation, question management, and user performance monitoring. The platform features a responsive Bootstrap 5 interface, supports both fixed and random question selection, includes timed quizzes, and offers comprehensive result tracking. The business vision is to provide an engaging and educational platform for users to test their knowledge across various subjects, with potential for market expansion into e-learning and corporate training modules.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### UI/UX Decisions
The application uses Bootstrap 5.3.0 for a responsive and modern user interface, ensuring a professional appearance across devices. All templates are designed with Bootstrap 5 components.

### Technical Implementations
- **Backend Framework**: Django 5.2.7 handles all backend logic, routing, and database interactions.
- **Database**: SQLite is used as the lightweight relational database, managed via Django ORM. For production deployments on platforms like Vercel, PostgreSQL is supported via `dj-database-url` and `psycopg2-binary`.
- **Authentication & Authorization**: Utilizes Django's built-in authentication system for user management, complemented by `@login_required` decorators and `user_passes_test` for access control. A `UserProfile` model extends Django's default `User` model.
- **Data Models**: Core models include `UserProfile`, `Quiz`, `Question`, and `UserQuizAttempt`. `UserQuizAttempt` uses `JSONField` for flexible storage of quiz submissions.
- **Quiz Logic**: Supports random question selection (`order_by('?')`), session-based quiz taking with single-question-at-a-time display, JavaScript-based countdown timers with auto-submit, and percentage-based scoring. Question IDs are persisted to ensure consistent grading for random quizzes.
- **Admin Panel**: Provides a protected interface for staff/superusers to manage users, quizzes (CRUD operations with inline question forms), and view detailed quiz results.
- **Dynamic Forms**: JavaScript dynamically generates question fields during quiz creation based on the "Total Questions Available" input.
- **One-Question-at-a-Time Quiz Flow**: Questions are displayed individually with navigation buttons (Previous, Next, Submit) and a progress bar. Answers are preserved when navigating.
- **Management Commands**: Includes a `setup_initial_data` command to populate the database with a superuser and sample quizzes.

### Feature Specifications
- **User Features**: Registration/authentication, quiz listing, timed quiz taking (fixed/random questions), automatic scoring, detailed results with explanations, quiz history, and profile editing.
- **Admin Features**: Protected admin panel dashboard (statistics, user management, quiz CRUD, results filtering, detailed results view).
- **Security Features**: CSRF protection, password hashing, form validation, and `@login_required` decorators.
- **Deployment Configuration**: Configured for Replit Autoscale deployment using Gunicorn and WhiteNoise for static files. Also supports Vercel deployment with PostgreSQL, including `vercel.json` and `build.sh` scripts.

## External Dependencies

### Frontend Libraries
- **Bootstrap 5.3.0**: CSS framework for responsive design and interactive components (via CDN).

### Python Packages
- **Django 5.2.7**: Core web framework.
- **Gunicorn**: WSGI HTTP Server for production deployment.
- **WhiteNoise**: Static file serving for Django applications in production.
- **psycopg2-binary**: PostgreSQL adapter for Python (for Vercel deployment).
- **dj-database-url**: Simplifies Django database URL configuration (for Vercel deployment).

### Database
- **SQLite**: Default development database.
- **PostgreSQL**: Recommended for production environments like Vercel.