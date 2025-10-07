from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quiz_site.quiz_app.models import Quiz, Question, UserProfile

class Command(BaseCommand):
    help = 'Setup initial superuser and sample quizzes'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(email='Gnanesh@gmail.com').exists():
            user = User.objects.create_superuser(
                username='Gnanesh',
                email='Gnanesh@gmail.com',
                password='Gnanesh@1561',
                first_name='Gnanesh',
                last_name='Admin'
            )
            UserProfile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists.'))
            user = User.objects.get(email='Gnanesh@gmail.com')

        if not Quiz.objects.filter(name='Git and Docker Basics').exists():
            quiz1 = Quiz.objects.create(
                name='Git and Docker Basics',
                description='Test your knowledge of version control with Git and containerization with Docker.',
                time_limit=15,
                num_questions=5,
                total_questions=5,
                quiz_type='fixed',
                created_by=user,
                is_active=True
            )

            questions1 = [
                {
                    'text': 'What is the primary purpose of Git?',
                    'option_a': 'Version control system for tracking changes in source code',
                    'option_b': 'A programming language',
                    'option_c': 'A web server',
                    'option_d': 'A database management system',
                    'correct_option': 'A',
                    'explanation': 'Git is a distributed version control system designed to track changes in source code during software development.'
                },
                {
                    'text': 'Which command is used to initialize a new Git repository?',
                    'option_a': 'git start',
                    'option_b': 'git init',
                    'option_c': 'git create',
                    'option_d': 'git new',
                    'correct_option': 'B',
                    'explanation': 'The "git init" command creates a new Git repository in the current directory.'
                },
                {
                    'text': 'What is Docker primarily used for?',
                    'option_a': 'Creating virtual machines',
                    'option_b': 'Containerization of applications',
                    'option_c': 'Web design',
                    'option_d': 'Network security',
                    'correct_option': 'B',
                    'explanation': 'Docker is a platform for developing, shipping, and running applications in containers.'
                },
                {
                    'text': 'Which file is used to define a Docker container\'s configuration?',
                    'option_a': 'config.yaml',
                    'option_b': 'Dockerfile',
                    'option_c': 'container.json',
                    'option_d': 'docker.xml',
                    'correct_option': 'B',
                    'explanation': 'A Dockerfile is a text document that contains all the commands needed to build a Docker image.'
                },
                {
                    'text': 'What command is used to commit changes in Git?',
                    'option_a': 'git save',
                    'option_b': 'git push',
                    'option_c': 'git commit',
                    'option_d': 'git update',
                    'correct_option': 'C',
                    'explanation': 'The "git commit" command records changes to the repository with a descriptive message.'
                }
            ]

            for q in questions1:
                Question.objects.create(quiz=quiz1, **q)

            self.stdout.write(self.style.SUCCESS('Quiz "Git and Docker Basics" created!'))

        if not Quiz.objects.filter(name='Python Programming Fundamentals').exists():
            quiz2 = Quiz.objects.create(
                name='Python Programming Fundamentals',
                description='Evaluate your understanding of Python basics and programming concepts.',
                time_limit=20,
                num_questions=5,
                total_questions=7,
                quiz_type='random',
                created_by=user,
                is_active=True
            )

            questions2 = [
                {
                    'text': 'Which of the following is the correct way to declare a variable in Python?',
                    'option_a': 'var x = 10',
                    'option_b': 'int x = 10',
                    'option_c': 'x = 10',
                    'option_d': 'declare x = 10',
                    'correct_option': 'C',
                    'explanation': 'Python uses dynamic typing, so you simply assign a value to a variable name without specifying its type.'
                },
                {
                    'text': 'What is the output of: print(type([]))?',
                    'option_a': '<class \'list\'>',
                    'option_b': '<class \'array\'>',
                    'option_c': '<class \'tuple\'>',
                    'option_d': '<class \'dict\'>',
                    'correct_option': 'A',
                    'explanation': 'Empty square brackets [] create a list object in Python.'
                },
                {
                    'text': 'Which keyword is used to create a function in Python?',
                    'option_a': 'function',
                    'option_b': 'def',
                    'option_c': 'func',
                    'option_d': 'define',
                    'correct_option': 'B',
                    'explanation': 'The "def" keyword is used to define a function in Python.'
                },
                {
                    'text': 'What does the len() function do?',
                    'option_a': 'Returns the length of an object',
                    'option_b': 'Creates a new list',
                    'option_c': 'Sorts a list',
                    'option_d': 'Converts to integer',
                    'correct_option': 'A',
                    'explanation': 'The len() function returns the number of items in an object.'
                },
                {
                    'text': 'Which operator is used for exponentiation in Python?',
                    'option_a': '^',
                    'option_b': '**',
                    'option_c': 'exp',
                    'option_d': 'pow',
                    'correct_option': 'B',
                    'explanation': 'The ** operator is used for exponentiation (e.g., 2**3 = 8).'
                },
                {
                    'text': 'What is the correct way to create a dictionary in Python?',
                    'option_a': 'dict = []',
                    'option_b': 'dict = ()',
                    'option_c': 'dict = {}',
                    'option_d': 'dict = <>',
                    'correct_option': 'C',
                    'explanation': 'Curly braces {} are used to create a dictionary in Python.'
                },
                {
                    'text': 'Which statement is used to handle exceptions in Python?',
                    'option_a': 'catch',
                    'option_b': 'except',
                    'option_c': 'handle',
                    'option_d': 'error',
                    'correct_option': 'B',
                    'explanation': 'The try-except block is used for exception handling, where "except" catches the exceptions.'
                }
            ]

            for q in questions2:
                Question.objects.create(quiz=quiz2, **q)

            self.stdout.write(self.style.SUCCESS('Quiz "Python Programming Fundamentals" created!'))

        self.stdout.write(self.style.SUCCESS('Initial data setup completed successfully!'))
